from django.http.response import JsonResponse
from .models import Venta, DetalleVenta
from .forms import VentaForm
from telas.models import Tela
from clientes.models import Cliente
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from datetime import datetime
from django.db import transaction


class VentaView(LoginRequiredMixin, generic.ListView):
    model = Venta 
    template_name = "ventas/ventas_list.html"
    login_url = 'bases:login'

    def queryset(self):
        ventas = Venta.objects.filter(fecha_eliminacion__isnull=True)
        fecha_desde = self.request.POST['fecha_desde']
        fecha_hasta = self.request.POST['fecha_hasta']
        ventas = ventas.filter(fecha_venta__range=(fecha_desde,fecha_hasta))
        cliente = self.request.POST['cliente']
        condicion_venta = self.request.POST['condicion_venta']
        if cliente:
            ventas = ventas.filter(cliente_razon_social__icontains=cliente)
       
        if condicion_venta:
            ventas = ventas.filter(condicion_venta=condicion_venta)
        
        return ventas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        context['fecha_hasta'] = datetime.now().strftime("%Y-%m-%d")
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                ventas = self.queryset()
                for venta in ventas:
                    data.append(venta.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)


class VentaCreate(LoginRequiredMixin, generic.CreateView):
    model=Venta
    form_class=VentaForm
    template_name="ventas/venta_form.html"
    success_url=reverse_lazy("ventas:ventas_list")
    login_url="bases:login"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_tela':
                data = []
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']))
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo + ' MET: ' + str(tela.metraje)
                    data.append(item)
            elif action == 'add':
                request_venta = json.loads(request.POST['venta'])
                with transaction.atomic():
                    venta = Venta()
                    cliente = Cliente.objects.get(pk=request_venta['cliente'])
                    venta.cliente_id = request_venta['cliente']
                    venta.cliente_razon_social = cliente.razon_social
                    venta.fecha_venta = request_venta['fecha_venta']
                    venta.condicion_venta = request_venta['condicion_venta']
                    venta.user_created_id = self.request.user.id
                    venta.save()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    for det in request_venta['telas']:
                        detalle =  DetalleVenta()
                        detalle.venta_id = venta.id
                        detalle.tela_id = det['id']
                        detalle.metraje_vendido = float(det['metraje_vendido'])
                        detalle.precio_unitario = int(det['precio_venta'])
                        detalle.sub_total = float(det['metraje_vendido']) * int(det['precio_venta'])
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        tela = Tela.objects.get(pk=detalle.tela_id)
                        tela.metraje -=  detalle.metraje_vendido
                        tela.save()
                        detalle.save()

                    venta.monto_total = monto_total
                    venta.total_iva_10 = total_iva_10
                    venta.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)