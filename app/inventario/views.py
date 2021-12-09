from django.core.checks.messages import INFO
from django.shortcuts import render
from django.views import generic
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from bases.mixins import ValidatePermissionRequired
from .forms import InventarioForm
from telas.models import Tela, TelaOferta
from inventario.models import Inventario, DetalleInventario
from user.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from datetime import datetime, date
from django.db import transaction
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class InventarioView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    model = Inventario
    permission_required = 'inventario.view_inventario'
    template_name = "inventario/inventario_list.html"
    login_url = 'bases:login'

    def queryset(self):
        inventarios = Inventario.objects.filter(fecha_eliminacion__isnull=True)
        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
        inventarios = inventarios.filter(fecha_inventario__range=(fecha_desde,fecha_hasta))
        return inventarios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado del Inventario'
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_hasta'] = datetime.now().strftime("%d/%m/%Y")
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                inventarios = self.queryset()
                for inventario in inventarios:
                    data.append(inventario.toJSON())
            elif request.POST['action'] == 'ajuste_inventario':
                id=request.POST['id']
                detalles = DetalleInventario.objects.filter(inventario_id=id)
                inventario = Inventario.objects.filter(id=id).first()
                inventario.fecha_ajuste = datetime.now()
                inventario.user_updated_id = self.request.user.id
                for det in detalles:
                    if( det.es_oferta == True):
                        print(det.es_oferta)
                        tela_oferta = TelaOferta.objects.get(estado=True, tela_id = det.tela_id)
                        tela_oferta.metraje_oferta = det.metraje_deposito
                        tela_oferta.save()
                    else:
                        tela = Tela.objects.get(id=det.tela_id)
                        tela.metraje =  det.metraje_deposito
                        tela.save()                    

                inventario.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class InventarioCreate(LoginRequiredMixin,ValidatePermissionRequired, generic.CreateView):
    model=Inventario
    permission_required = 'inventario.add_inventario'
    form_class=InventarioForm
    template_name="inventario/inventario_form.html"
    success_url=reverse_lazy("inventario:inventario_list")
    login_url="bases:login"

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_tela':
                data = []
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']))
                telas_oferta = TelaOferta.objects.select_related('tela').filter(Q(tela__codigo__icontains=request.POST['term']) | Q(tela__nombre__icontains=request.POST['term']), estado=True)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo
                    data.append(item)

                for tela_oferta in telas_oferta:
                    aux = tela_oferta.toJSON()
                    aux['text'] = 'TELA: '+ tela_oferta.tela.nombre + ' '+ tela_oferta.descripcion + ' COD: ' + tela_oferta.tela.codigo
                    data.append(aux)
            elif action == 'add':
                request_inventario = json.loads(request.POST['inventario'])
                with transaction.atomic():
                    inventario = Inventario()
                    inventario.fecha_inventario = str(request_inventario['fecha_inventario'])
                    inventario.fecha_inventario = datetime.strptime(inventario.fecha_inventario, "%d/%m/%Y").strftime("%Y-%m-%d")
                    inventario.user_created_id = self.request.user.id
                    inventario.save()
                    
                    for det in request_inventario['telas']:
                        detalle =  DetalleInventario()
                        detalle.inventario_id = inventario.id
                        tela_id = det['id']
                        if (det['oferta'] == 1):
                            detalle.descripcion = det['nombre']  + ' ' + det['codigo'] + ' ' +det['descripcion']
                            tela_id = det['tela_id']
                        else:
                            detalle.descripcion = det['nombre']  + ' '  + det['codigo']
                        detalle.tela_id = tela_id
                        detalle.metraje_deposito = float(det['metraje_deposito'])

                        if (det['oferta'] == 1):
                            tela_oferta = TelaOferta.objects.get(estado=True, id = det['id'] )
                            if (tela_oferta.metraje_oferta > detalle.metraje_deposito):
                                detalle.es_oferta = True
                                detalle.ultimo_metraje = tela_oferta.metraje_oferta
                                detalle.metraje_ajustado = tela_oferta.metraje_oferta - detalle.metraje_deposito
                                detalle.monto_perdida = (tela_oferta.metraje_oferta - detalle.metraje_deposito) * tela_oferta.precio_oferta
                            else:
                                detalle.es_oferta = True
                                detalle.ultimo_metraje = tela_oferta.metraje_oferta
                                detalle.metraje_ajustado = detalle.metraje_deposito - tela_oferta.metraje_oferta
                                detalle.monto_perdida = (detalle.metraje_deposito - tela_oferta.metraje_oferta) * tela_oferta.precio_oferta
                        
                        else:
                            tela = Tela.objects.get(pk=detalle.tela_id)
                            if (tela.metraje > detalle.metraje_deposito):
                                detalle.ultimo_metraje = tela.metraje
                                detalle.metraje_ajustado = tela.metraje - detalle.metraje_deposito
                                detalle.monto_perdida = (tela.metraje - detalle.metraje_deposito) * tela.precio_venta
                            else:
                                detalle.ultimo_metraje = tela.metraje
                                detalle.metraje_ajustado = detalle.metraje_deposito - tela.metraje
                                detalle.monto_perdida = (detalle.metraje_deposito - tela.metraje) * tela.precio_venta


                        detalle.user_created_id = self.request.user.id
                        #tela = Tela.objects.get(pk=detalle.tela_id)
                        #tela.metraje -=  detalle.metraje_vendido
                        #tela.save()
                        detalle.save()
                    
                    data = {'id': inventario.id}
                    inventario.save()

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class InventarioListadoPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:

            template = get_template('inventario/listado_pdf.html')
            context = {
                'inventarios': Inventario.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inventario:inventario_list'))

class InventarioListadoCompletoPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            inventarios = Inventario.objects.get(pk=self.kwargs['pk'])
            usuario_inventario = inventarios.user_updated_id
            usuario = User.objects.get(id=usuario_inventario)
            metraje = DetalleInventario.objects.filter(id=self.kwargs['pk'])
            template = get_template('inventario/listado_completo_pdf.html')
            context = {
                'inventarios': inventarios,
                'usuario': usuario,
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy('inventario:inventario_list'))