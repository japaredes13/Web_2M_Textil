from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignObject
from django.shortcuts import render, redirect
from django.db import transaction
from django.views import generic
from cajas.models import Caja, Pago, Banco
from cajas.forms import PagoForm, BancoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from bases.mixins import ValidatePermissionRequired
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime,date
from calendar import monthrange
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from reportlab.lib.utils import prev_this_next
from proveedores.models import Proveedor
from .forms import OrdenCompraForm, CompraForm
from telas.models import Tela
from configuracion.models import ConfiguracionUsuario
from .models import *

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class OrdenCompraListView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    model = OrdenCompra
    permission_required = 'compras.view_ordencompra'
    template_name = 'orden_compras/orden_compras_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def queryset(self):
        orden_compras = OrdenCompra.objects.select_related('proveedor').filter(fecha_eliminacion__isnull=True)
        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")

        orden_compras = orden_compras.filter(fecha_orden__range=(fecha_desde,fecha_hasta))
        proveedor = self.request.POST['proveedor']
        if proveedor:
            orden_compras = orden_compras.filter(proveedor__nombre_empresa__icontains=proveedor)
        return orden_compras

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'searchdata':
                data = []
                orden_compras = self.queryset()
                for orden_compra in orden_compras:
                    data.append(orden_compra.toJSON())
            elif action == 'search_details_telas':
                data = []
                for i in DetalleOrdenCompra.objects.filter(orden_compra_id=request.POST['id']):
                    data.append(i.toJSON())
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Orden de Compras'
        context['create_url'] = reverse_lazy('compras:orden_compra_create')
        context['list_url'] = reverse_lazy('compras:orden_compra_list')
        context['entity'] = 'Orden de Compras'
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_hasta'] = datetime.now().strftime("%d/%m/%Y")
        return context


class OrdenCompraCreateView(LoginRequiredMixin,ValidatePermissionRequired, generic.CreateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    permission_required = 'compras.add_ordencompra'
    template_name = 'orden_compras/orden_compras_form.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'search_telas':
                filtro = request.POST['filtro']
                data = []
                configuracion = ConfiguracionUsuario.objects.filter(estado=True).values('metraje_minimo').first()
                #print(configuracion['metraje_minimo'])
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']),fecha_eliminacion__isnull=True)
                
                if filtro == 'metraje_minimo':
                    telas = telas.filter(metraje__lt=int(configuracion['metraje_minimo']))
                elif filtro == 'metraje_normal':
                    telas = telas.filter(metraje__gte=int(configuracion['metraje_minimo']))
                
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo + ' MET: ' + str(tela.metraje)
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    request_orden_compra = json.loads(request.POST['orden_compras'])
                    orden_compra = OrdenCompra()
                    orden_compra.proveedor_id = request_orden_compra['proveedor']
                    orden_compra.fecha_orden = str(request_orden_compra['fecha_orden'])
                    orden_compra.fecha_orden = datetime.strptime(orden_compra.fecha_orden, "%d/%m/%Y").strftime("%Y-%m-%d")
                    orden_compra.user_created_id = self.request.user.id
                    orden_compra.estado = False
                    orden_compra.save()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    for det in request_orden_compra['telas']:
                        detalle = DetalleOrdenCompra()
                        detalle.orden_compra_id = orden_compra.id
                        detalle.tela_id = det['id']
                        detalle.metraje = float(det['metraje'])
                        detalle.precio_unitario = int(det['precio_unitario'])
                        detalle.sub_total = round(float(det['metraje']) * int(det['precio_unitario']))
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        detalle.save()

                    orden_compra.monto_total = monto_total
                    orden_compra.total_iva_10 = total_iva_10
                    orden_compra.save()
 
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Orden de Compra'
        context['entity'] = 'Orden de Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['detalles'] = []
        return context


class OrdenCompraUpdateView(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    permission_required = 'compras.change_ordencompra'
    template_name = 'orden_compras/orden_compras_form.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_telas':
                data = []
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']),fecha_eliminacion__isnull=True,metraje__lt=100)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo + ' MET: ' + str(tela.metraje)
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    request_orden_compra = json.loads(request.POST['orden_compras'])
                    orden_compra = OrdenCompra.objects.get(id=self.get_object().id)
                    orden_compra.proveedor_id = request_orden_compra['proveedor']
                    orden_compra.fecha_orden = str(request_orden_compra['fecha_orden'])
                    orden_compra.fecha_orden = datetime.strptime(orden_compra.fecha_orden, "%d/%m/%Y").strftime("%Y-%m-%d")
                    orden_compra.user_updated_id = self.request.user.id
                    orden_compra.estado = False
                    orden_compra.save()
                    orden_compra.detalleordencompra_set.all().delete()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    for det in request_orden_compra['telas']:
                        detalle = DetalleOrdenCompra()
                        detalle.orden_compra_id = orden_compra.id
                        detalle.tela_id = det['id']
                        detalle.metraje = float(det['metraje'])
                        detalle.precio_unitario = int(det['precio_unitario'])
                        detalle.sub_total = round(float(det['metraje']) * int(det['precio_unitario']))
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = orden_compra.user_created_id
                        detalle.user_updated_id = self.request.user.id
                        detalle.save()

                    orden_compra.monto_total = monto_total
                    orden_compra.total_iva_10 = total_iva_10
                    orden_compra.save()
 
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Orden de Compra'
        context['entity'] = 'Orden de Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detalles'] = json.dumps(self.get_details_product())
        return context

    def get_details_product(self):
        data = []
        try:
            for i in DetalleOrdenCompra.objects.filter(orden_compra_id=self.get_object().id):
                item = i.tela.toJSON()
                item['precio_unitario'] = i.precio_unitario
                item['metraje'] = i.metraje
                item['sub_total'] = i.sub_total
                data.append(item)
        except:
            pass
        print(data)
        return data

class OrdenCompraDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = OrdenCompra
    template_name = 'compras/delete.html'
    success_url = reverse_lazy('compras:orden_compras_list')
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
        context['title'] = 'Eliminación de una Orden de Compra'
        context['entity'] = 'Orden de Compras'
        context['list_url'] = self.success_url
        return context


class CompraListView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    model = Compra
    permission_required = 'compras.view_compra'
    template_name = 'compras/compras_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def queryset(self):
        compras = Compra.objects.filter(fecha_eliminacion__isnull=True)
        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
        compras = compras.filter(fecha_compra__range=(fecha_desde,fecha_hasta))
        proveedor = self.request.POST['proveedor']
        if proveedor:
            compras = compras.filter(proveedor__nombre_empresa__icontains=proveedor)
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
            elif action == 'edit_cuota':
                #print("HOLASA MAMASA")
                estado=request.POST['estado'] 
                medio_pago = (request.POST['medio_pago'] )
                banco = (request.POST['banco'] )
                cuota_id=request.POST['id'] 
                cuota=CuotaCompra.objects.get(id=cuota_id)
                caja = Caja.objects.get(estado=True)
                cuota.estado =  True
                cuota.fecha_cancelacion = datetime.now()
                cuota.save()

                pago = Pago()
                pago.compra_id = cuota.compra_id
                pago.cuota_id = cuota_id
                pago.caja_id = caja.id
                pago.fecha_pago = cuota.fecha_cancelacion
                pago.medio_pago = medio_pago
                pago.user_created_id = self.request.user.id
                if (medio_pago=='Cheque'):
                    pago.monto_pagado = cuota.monto_cuota
                    pago.banco_id = banco
                    caja.monto_cheque -= cuota.monto_cuota
                    print(caja.monto_cheque)
                    print(cuota.monto_cuota)

                else:
                    pago.monto_pagado = cuota.monto_cuota
                    caja.monto_efectivo -= cuota.monto_cuota
                    caja.monto_actual -= cuota.monto_cuota
                caja.save()
                pago.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['list_url'] = reverse_lazy('compras:compras_list')
        context['entity'] = 'Compras'
        context['fecha_compra'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_hasta'] = datetime.now().strftime("%d/%m/%Y")
        context ["bancos"] = Banco.objects.filter(estado=True)
        return context


class CompraCreateView(LoginRequiredMixin, ValidatePermissionRequired, generic.UpdateView):
    model = OrdenCompra
    form_class = CompraForm
    permission_required = 'compras.add_compra'
    template_name = 'compras/compras_form.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        caja = Caja.objects.filter(estado=True).first()
        if (caja): 
            pass
        else:
            messages.error(self.request, 'No existe una caja para operar. Por favor abra la caja para comprar.')
            return HttpResponseRedirect(reverse_lazy('compras:compras_list'))

        return super().render_to_response(context, **response_kwargs)

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
                caja = Caja.objects.filter(estado=True).values('monto_actual').first()
                monto_total = int(request.POST['monto_total'])
                request_compra = json.loads(request.POST['compras'])
                medio_pago = request_compra['medio_pago']
                data = []
                item = {}
                print (int(caja['monto_actual']) < monto_total)
                if( int(caja['monto_actual']) < monto_total and medio_pago=='Efectivo'):
                    item['error'] = True
                    item['message'] = 'El monto a pagar supera al de la caja'
                    data.append(item)
                    return JsonResponse(data, safe=False)

                with transaction.atomic():
                    
                    
                    orden_compra = OrdenCompra.objects.get(id=self.get_object().id)
                    orden_compra.estado = True
                    orden_compra.save()

                    compra = Compra()
                    proveedor = Proveedor.objects.get(pk=request_compra['proveedor'])
                    compra.proveedor_id = request_compra['proveedor']
                    compra.proveedor_nombre = proveedor.nombre_empresa
                    compra.nro_factura = request_compra['nro_factura']
                    compra.timbrado = request_compra['timbrado']
                    compra.fecha_compra = str(request_compra['fecha_compra'])
                    compra.fecha_compra = datetime.strptime(compra.fecha_compra, "%d/%m/%Y").strftime("%Y-%m-%d")
                    compra.inicio_timbrado = str(request_compra['inicio_timbrado'])
                    compra.inicio_timbrado = datetime.strptime(compra.inicio_timbrado, "%d/%m/%Y").strftime("%Y-%m-%d")
                    compra.fin_timbrado = str(request_compra['fin_timbrado'])
                    compra.fin_timbrado = datetime.strptime(compra.fin_timbrado, "%d/%m/%Y").strftime("%Y-%m-%d")
                    compra.condicion_compra = request_compra['condicion_compra']
                    compra.medio_pago = request_compra['medio_pago']
                    compra.plazo = request_compra['plazo']
                    compra.numero_cheque = request_compra['numero_cheque']
                    compra.user_created_id = self.request.user.id
                    compra.save()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    for det in request_compra['telas']:
                        detalle = DetalleCompra()
                        detalle.compra_id = compra.id
                        detalle.tela_id = det['id']
                        detalle.metraje_comprado = float(det['metraje_comprado'])
                        detalle.precio_costo = int(det['precio_costo'])
                        detalle.sub_total = round(float(det['metraje_comprado']) * int(det['precio_costo']))
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        detalle.save()

                        detalle.tela.metraje += detalle.metraje_comprado
                        detalle.tela.precio_compra_anterior = detalle.tela.precio_compra
                        detalle.tela.precio_compra = detalle.precio_costo
                        detalle.tela.precio_venta = detalle.tela.precio_compra + (0.30 * detalle.tela.precio_compra)
                        detalle.tela.save()
                    compra.monto_total = monto_total
                    compra.total_iva_10 = total_iva_10
                    compra.save()

                    caja = Caja.objects.get(estado=True)
                    #if (compra.medio_pago=='Cheque'):
                    #    caja.monto_cheque -= compra.monto_total
                    #    caja.save()

                    #if (compra.medio_pago=='Efectivo'):
                    #    caja.monto_efectivo -= compra.monto_total
                    #    caja.monto_actual -= compra.monto_total
                    #    caja.save()

                    if (compra.condicion_compra=='contado'):
                        pago = Pago()
                        pago.compra_id = compra.id
                        pago.caja_id = caja.id
                        pago.monto_pagado = compra.monto_total
                        pago.medio_pago = compra.medio_pago
                        pago.user_created_id = self.request.user.id
                        pago.fecha_pago = compra.fecha_compra
                        if (pago.medio_pago=='Efectivo'):
                            caja.monto_efectivo -= compra.monto_total
                            caja.monto_actual -= compra.monto_total
                        if (pago.medio_pago=='Cheque'):
                            nombre_banco = Banco.objects.get(pk=request_compra['banco'])                    
                            pago.banco = nombre_banco
                            caja.monto_cheque -= compra.monto_total
                            pago.numero_cheque = compra.numero_cheque
                        pago.save()
                        caja.save()

                    if (compra.condicion_compra=='credito'):
                        compra.plazo = request_compra['plazo']
                        cantidad = int(int(compra.plazo)/30)
                        monto = int(int(compra.monto_total)/cantidad)
                        for i in range(cantidad):
                            deuda = CuotaCompra()
                            deuda.compra_id = compra.id
                            deuda.numero_cuota = i+1
                            deuda.monto_cuota = monto
                            deuda.fecha_vencimiento =  datetime.now() + relativedelta(months=i+1)
                            deuda.user_created_id = self.request.user.id
                            deuda.estado = False
                            deuda.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            
            #CAMBIAR EL MENSAJE DE ERROR
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetalleOrdenCompra.objects.filter(orden_compra_id=self.get_object().id):
                item = i.tela.toJSON()
                item['precio_costo'] = i.precio_unitario
                item['metraje_comprado'] = i.metraje
                item['sub_total'] = i.sub_total
                data.append(item)
        except:
            pass
        return data
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['proveedor'] = self.get_object().proveedor_id
        context ["bancos"] = Banco.objects.filter(estado=True)
        context['detalles'] = json.dumps(self.get_details_product())
        return context


class CompraUpdateView(LoginRequiredMixin, generic.UpdateView):
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
            elif action == 'edit':
                with transaction.atomic():
                    request_compra = json.loads(request.POST['compras'])
                    compra = self.get_object()
                    compra.proveedor_id = request_compra['proveedor']
                    compra.nro_factura = request_compra['nro_factura']
                    compra.timbrado = request_compra['timbrado']
                    compra.fecha_compra = request_compra['fecha_compra']
                    compra.condicion_venta = request_compra['condicion_compra']
                    compra.user_created_id = self.request.user.id
                    compra.save()
                    
                    monto_total = 0
                    total_iva_10 = 0
                    compra.detallecompra_set.all().delete()
                    for det in request_compra['telas']:
                        detalle = DetalleCompra()
                        detalle.compra_id = compra.id
                        detalle.tela_id = det['id']
                        detalle.metraje_comprado = float(det['metraje_comprado'])
                        detalle.precio_costo = int(det['precio_costo'])
                        detalle.sub_total = round(float(det['metraje_comprado']) * int(det['precio_costo']))
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

    def get_details_product(self):
        data = []
        try:
            for i in DetalleCompra.objects.filter(compra_id=self.get_object().id):
                item = i.tela.toJSON()
                item['precio_costo'] = i.precio_costo
                item['metraje_comprado'] = i.metraje_comprado
                item['sub_total'] = i.sub_total
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
        context['detalles'] = json.dumps(self.get_details_product())
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


class OrdenCompraPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            orden_compras = OrdenCompra.objects.filter(fecha_eliminacion__isnull=True)

            fecha_desde = str(self.request.GET['fecha_desde'])
            fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
            fecha_hasta = str(self.request.GET['fecha_hasta'])
            fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")

            proveedor = request.GET['proveedor']
            if proveedor:
                orden_compras = orden_compras.filter(proveedor__nombre_empresa__icontains=proveedor,fecha_orden__range=(fecha_desde,fecha_hasta))
            else:
                orden_compras = orden_compras.filter(fecha_orden__range=(fecha_desde,fecha_hasta))

            template = get_template('orden_compras/listado_pdf.html')
            context = {
                'orden_compras': orden_compras
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compras:orden_compras_list'))

class CompraPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            compras = Compra.objects.filter(fecha_eliminacion__isnull=True)

            fecha_desde = str(self.request.GET['fecha_desde'])
            fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
            fecha_hasta = str(self.request.GET['fecha_hasta'])
            fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")

            proveedor = request.GET['proveedor']
            if proveedor:
                compras = compras.filter(proveedor__nombre_empresa__icontains=proveedor,fecha_compra__range=(fecha_desde,fecha_hasta))
            else:
                compras = compras.filter(fecha_compra__range=(fecha_desde,fecha_hasta))

            template = get_template('compras/listado_pdf.html')
            context = {
                'compras': compras
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('compras:compras_list'))

class CompraListadoDetallePdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:

            template = get_template('compras/listado_detalles_pdf.html')
            context = {
                'compras': Compra.objects.get(pk=self.kwargs['pk'])
            }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compras:compra_list'))

class CompraPago(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    model = CuotaCompra
    permission_required = 'compras.view_pago'
    template_name = "compras/compras_pago_list.html"
    login_url = 'bases:login'

    def queryset(self):

        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")

        deudas = CuotaCompra.objects.select_related('compra').filter(fecha_vencimiento__range=(fecha_desde,fecha_hasta))
        deudas = deudas.filter(estado=False)
        proveedor = self.request.POST['proveedor']
        if proveedor:
            deudas = deudas.filter(Q(compra__proveedor_nombre__icontains=proveedor)| Q(compra__nro_factura__icontains=proveedor))
        return deudas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuotas a Vencer'
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_hasta'] = self.last_day_of_month(datetime.now()).strftime("%d/%m/%Y")
        return context

    def last_day_of_month(self,date_value):
        return date_value.replace(day = monthrange(date_value.year, date_value.month)[1])


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                deudas = self.queryset()
                for deuda in deudas:
                    data.append(deuda.toJSON())

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)