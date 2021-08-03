from django.shortcuts import render, redirect
from django.db import transaction
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.db.models import Q
from proveedores.models import Proveedor
from .forms import CompraForm
from telas.models import Tela
from .models import Compra, DetalleCompra


class CompraListView(LoginRequiredMixin, generic.ListView):
    model = Compra
    template_name = 'compras/compras_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def queryset(self):
        compras = Compra.objects.filter(fecha_eliminacion__isnull=True)
        fecha_desde = self.request.POST['fecha_desde']
        fecha_hasta = self.request.POST['fecha_hasta']
        compras = compras.filter(fecha_compra__range=(fecha_desde,fecha_hasta))
        return compras

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                compras = self.queryset()
                for compra in compras:
                    data.append(compra.toJSON())
            elif action == 'search_details_telas':
                data = []
                for i in DetalleCompra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('compras:compra_create')
        context['list_url'] = reverse_lazy('compras:compra_list')
        context['entity'] = 'Compras'
        context['fecha_desde'] = datetime.now().strftime("%Y-%m-%d")
        context['fecha_hasta'] = datetime.now().strftime("%Y-%m-%d")
        return context


class CompraCreateView(LoginRequiredMixin, generic.CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compras_form.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_telas':
                data = []
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']))
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = tela.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    request_compra = json.loads(request.POST['compras'])
                    print(request_compra)
                    compra = Compra()
                    compra.proveedor_id = request_compra['proveedor']
                    compra.nro_factura = request_compra['nro_factura']
                    compra.timbrado = request_compra['timbrado']
                    compra.fecha_compra = request_compra['fecha_compra']
                    compra.condicion_venta = request_compra['condicion_compra']
                    compra.user_created_id = self.request.user.id
                    compra.save()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    for det in request_compra['telas']:
                        detalle = DetalleCompra()
                        detalle.compra_id = compra.id
                        detalle.tela_id = det['id']
                        detalle.metraje_comprado = float(det['metraje_comprado'])
                        detalle.precio_costo = int(det['precio'])
                        detalle.sub_total = round(float(det['metraje_comprado']) * int(det['precio']))
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        detalle.save()

                    compra.monto_total = monto_total
                    compra.total_iva_10 = total_iva_10
                    compra.save()
 
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class CompraUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compras_form.html'
    success_url = reverse_lazy('compras:compras_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_telas':
                data = []
                telas = Tela.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in telas:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    compras = json.loads(request.POST['compras'])
                    #compra = Compra.objects.get(pk=self.get_object().id)
                    compra = self.get_object()
                    compra.date_joined = compras['date_joined']
                    compra.prov_id = compras['prov']
                    compra.subtotal = float(compras['subtotal'])
                    compra.iva = float(compras['iva'])
                    compra.total = float(compras['total'])
                    compra.save()
                    compra.detcompra_set.all().delete()
                    for i in compras['telas']:
                        det = DetalleCompra()
                        det.compra_id = compra.id
                        det.telas_id = i['id']
                        det.metraje = int(i['metraje'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_telas(self):
        data = []
        try:
            for i in DetalleCompra.objects.filter(compra_id=self.get_object().id):
                item = i.telas.toJSON()
                item['metraje'] = i.metraje
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_telas())
        return context


class CompraDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Compra
    template_name = 'compras/delete.html'
    success_url = reverse_lazy('compras:compras_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        return context