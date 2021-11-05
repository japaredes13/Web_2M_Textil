from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from .models import  Caja, Banco, Cobro, Movimiento, Pago
from configuracion.models import ConfiguracionEgreso
from .forms import CajaForm, BancoForm, CobroForm
from ventas.models import Venta
from .forms import CajaForm, CajaMovimientoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.db.models import Sum

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class CajaList(LoginRequiredMixin,generic.ListView):
    model = Caja 
    template_name = "cajas/caja_list.html"
    login_url = 'bases:login'

    def queryset(self):
        cajas = Caja.objects.filter(fecha_eliminacion__isnull=True)
        buscar_caja = self.request.POST['caja']
        if buscar_caja:
            cajas = cajas.filter(Q(user_created__icontains=buscar_caja))
        return cajas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                cajas = self.queryset()
                for caja in cajas:
                    data.append(caja.toJSON())
            elif request.POST['action'] == 'cerrar_caja':
                id=request.POST['id']
                caja = Caja.objects.get(id=id) 
                caja.estado = False
                caja.fecha_cierre = datetime.now()
                caja.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

class CajaCreate(LoginRequiredMixin, generic.CreateView):
    model=Caja
    template_name="cajas/caja_form.html"
    context_object_name="obj"
    form_class=CajaForm
    success_url=reverse_lazy("cajas:caja_list")
    login_url="bases:login"

    def render_to_response(self, context, **response_kwargs):
        caja = Caja.objects.filter(estado=True).first()
        if (caja): 
            messages.error(self.request, 'Ya existe una caja abierta. Por favor cierre la caja para crear una.')
            return HttpResponseRedirect(reverse_lazy('cajas:caja_list'))
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        form.instance.monto_actual = self.request.POST['monto_apertura']
        form.instance.monto_efectivo = self.request.POST['monto_apertura']
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, "Apertura de caja éxitosamente." )
        return super().form_valid(form)

    def form_invalid(self,form):
        print (form)
        return JsonResponse(form.errors, status=400)

    def get_context_data (self, **kwargs):
        context = super(CajaCreate,self).get_context_data(**kwargs)
        return context

class CajaEdit(LoginRequiredMixin, generic.UpdateView):
    model=Caja
    template_name="cajas/caja_form.html"
    context_object_name = 'obj'
    form_class=CajaForm
    success_url= reverse_lazy("cajas:caja_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

class BancoView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "cajas/bancos/banco_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = Banco.objects.filter(fecha_eliminacion__isnull=True).order_by('descripcion')
        return queryset


class BancoCreate(LoginRequiredMixin, generic.CreateView):
    model = Banco
    template_name="cajas/bancos/banco_form.html"
    context_object_name = 'obj'
    form_class=BancoForm
    success_url= reverse_lazy("cajas:banco_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class BancoEdit(LoginRequiredMixin, generic.UpdateView):
    model=Banco
    template_name="cajas/bancos/banco_form.html"
    context_object_name = 'obj'
    form_class=BancoForm
    success_url= reverse_lazy("cajas:banco_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

def banco_delete(request,id):
    try:
        banco= Banco.objects.get(pk=id)
        banco.fecha_eliminacion = datetime.now()
        banco.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Banco.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)

class CajaMovimientoList(LoginRequiredMixin,generic.ListView):
    model = Movimiento 
    template_name = "cajas/movimientos_list.html"
    login_url = 'bases:login'

    def queryset(self):
        movimientos = Movimiento.objects.select_related('caja').filter(fecha_eliminacion__isnull=True)
        movimientos = movimientos.filter(caja__estado=True)
        tipo_movimiento = self.request.POST['tipo_movimiento']
        if tipo_movimiento:
            movimientos = movimientos.filter(tipo_movimiento=tipo_movimiento)
        return movimientos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                movimientos = self.queryset()
                for movimiento in movimientos:
                    data.append(movimiento.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)


class CajaMovimientoCreate(LoginRequiredMixin, generic.CreateView):
    model = Movimiento
    template_name="cajas/movimientos_form.html"
    context_object_name="obj"
    form_class=CajaMovimientoForm
    success_url=reverse_lazy("cajas:movimientos_list")
    login_url="bases:login"

    def form_valid(self, form):
        caja = Caja.objects.filter(estado=True)
        if (caja.count() > 1):
            messages.error(self.request, "Hay más de una caja abierta." )
            return redirect("cajas:movimientos_list")
        
        if (caja.count() < 1):
            messages.error(self.request, "No existe una caja abierta." )
            return redirect("cajas:movimientos_list")
        
        caja = Caja.objects.filter(estado=True).first()
        
        if (self.request.POST['tipo_movimiento'] == 'ingreso'):
            caja.monto_ingreso += int(self.request.POST['monto'])
            caja.monto_actual += int(self.request.POST['monto'])

        if (self.request.POST['tipo_movimiento'] == 'egreso'):
            if (caja.monto_actual<int(self.request.POST['monto'])):
                messages.error(self.request, "EL monto debe ser menor a:" +str(caja.monto_actual))
                return redirect("cajas:movimiento_create")
            else:
                caja.monto_egreso += int(self.request.POST['monto'])
                caja.monto_actual -= int(self.request.POST['monto'])
        
        configuracion = ConfiguracionEgreso.objects.filter(estado=True).values('monto_maximo').first()
        monto_max = configuracion['monto_maximo']
        if (int(self.request.POST['monto'])>monto_max):
            messages.error(self.request, "EL monto debe ser menor a:" +str(monto_max))
            return redirect("cajas:movimiento_create")

        caja.save()
        form.instance.user_created = self.request.user
        form.instance.estado = True
        form.instance.caja_id = caja.id
        messages.success(self.request, "Movimiento creado éxitosamente." )
        return super().form_valid(form)


    def get_context_data (self, **kwargs):
        context = super(CajaMovimientoCreate,self).get_context_data(**kwargs)
        context['fecha_movimiento'] = datetime.now().strftime("%d/%m/%Y")
        return context


class CajaMovimientoEdit(LoginRequiredMixin, generic.UpdateView):
    model = Movimiento
    template_name="cajas/movimientos_form.html"
    context_object_name = 'obj'
    form_class=CajaMovimientoForm
    success_url=reverse_lazy("cajas:movimientos_list")
    login_url="bases:login"

    def form_valid(self, form):
        caja = Caja.objects.filter(estado=True)
        if (caja.count() > 1):
            messages.error(self.request, "Hay más de una caja abierta." )
            return redirect("cajas:movimientos_list")
        
        if (caja.count() < 1):
            messages.error(self.request, "No existe una caja abierta." )
            return redirect("cajas:movimientos_list")
        
        caja = Caja.objects.filter(estado=True).first()
        movimiento = Movimiento.objects.get(id=self.get_object().id)
        if (self.request.POST['tipo_movimiento'] == 'ingreso'):
            caja.monto_ingreso -= movimiento.monto
            caja.monto_ingreso += int(self.request.POST['monto'])
            caja.monto_actual -= movimiento.monto
            caja.monto_actual += int(self.request.POST['monto'])

        if (self.request.POST['tipo_movimiento'] == 'egreso'):
            caja.monto_egreso -= movimiento.monto
            caja.monto_egreso += int(self.request.POST['monto'])
            caja.monto_actual += movimiento.monto
            caja.monto_actual -= int(self.request.POST['monto'])
            
        
        caja.save()
        form.instance.user_updated = self.request.user
        form.instance.caja_id = caja.id
        messages.success(self.request, "Movimiento modificado éxitosamente." )
        print(super().form_valid(form))
        return super().form_valid(form)


    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(CajaMovimientoEdit,self).get_context_data(**kwargs)
        context ["obj"] = Movimiento.objects.filter(pk=pk).first()
        return context

class CajaListadoPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            cobros = Cobro.objects.select_related('venta').filter(caja_id=self.kwargs['pk'], venta__anulado=False)
            print(cobros)
            caja = Caja.objects.filter(id=self.kwargs['pk']).values('monto_actual','monto_apertura','fecha_cierre').first()
            pagos = Pago.objects.select_related('compra').filter(caja_id=self.kwargs['pk'])
            ingresos = Movimiento.objects.filter(caja_id=self.kwargs['pk'],tipo_movimiento='ingreso')
            egresos = Movimiento.objects.filter(caja_id=self.kwargs['pk'],tipo_movimiento='egreso')
            #cobros_efectivo = Cobro.objects.select_related('venta').filter(caja_id=self.kwargs['pk'],medio_cobro='Efectivo', venta__anulado=False)
            #cobros_cheque = Cobro.objects.select_related('venta').filter(caja_id=self.kwargs['pk'],medio_cobro='Cheque', venta__anulado=False)
            #monto_efectivo = cobros_efectivo.aggregate(Sum('monto_cobrado'))
            #monto_cheque = cobros_cheque.aggregate(Sum('monto_cobrado'))
            monto_total = cobros.aggregate(Sum('monto_cobrado'))
            monto_total_compra = pagos.aggregate(Sum('monto_pagado'))
            monto_ingreso = ingresos.aggregate(Sum('monto'))
            monto_egreso = egresos.aggregate(Sum('monto'))
            if ( monto_total['monto_cobrado__sum']==None): 
                monto_total['monto_cobrado__sum']=0
            if (monto_total_compra['monto_pagado__sum']==None):
                monto_total_compra['monto_pagado__sum']=0
            if (monto_ingreso['monto__sum']==None):
                monto_ingreso['monto__sum']=0
            if (monto_egreso['monto__sum']==None):
                monto_egreso['monto__sum']=0
            template = get_template('cajas/listado_pdf.html')
            context = {
                'cobros' : cobros,
                'pagos' : pagos,
                'ingresos' : ingresos,
                'egresos' : egresos,
                'monto_total' : monto_total,
                'monto_total_compra' : monto_total_compra,
                'monto_ingreso' : monto_ingreso,
                'monto_egreso' : monto_egreso,
                'saldo_actual' : caja['monto_actual'],
                'monto_apertura' : caja['monto_apertura'],
                'fecha_cierre' : caja['fecha_cierre']
            }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except Exception as e:
            print('hubo un error'+str(e))
            pass
        return HttpResponseRedirect(reverse_lazy('cajas:caja_list'))