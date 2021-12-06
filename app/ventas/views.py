from configuracion.models import ConfiguracionProducto, ConfiguracionVenta
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Venta, DetalleVenta, CuotaVenta
from .forms import VentaForm
from telas.models import Tela, TelaOferta
from cajas.models import Caja, Cobro, Banco
from cajas.forms import CobroForm, BancoForm
from clientes.models import Cliente
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from datetime import datetime, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.contrib import messages
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class VentaView(LoginRequiredMixin, generic.ListView):
    model = Venta 
    template_name = "ventas/ventas_list.html"
    login_url = 'bases:login'

    def queryset(self):
        ventas = Venta.objects.filter(fecha_eliminacion__isnull=True)
        print(ventas)
        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")
        ventas = ventas.filter(fecha_venta__range=(fecha_desde,fecha_hasta))
        cliente = self.request.POST['cliente']
        condicion_venta = self.request.POST['condicion_venta']
        if cliente:
            ventas = ventas.filter(Q(cliente_razon_social__icontains=cliente) |Q(nro_factura__icontains=cliente) )
       
        if condicion_venta:
            ventas = ventas.filter(condicion_venta=condicion_venta)
        
        return ventas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['fecha_desde'] = datetime.now().replace(day=1).strftime("%d/%m/%Y")
        context['fecha_hasta'] = datetime.now().strftime("%d/%m/%Y")
        context ["bancos"] = Banco.objects.filter(estado=True)
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
                print(ventas)
                if (request.POST['deuda_credito']=='deuda'):
                    for venta in ventas:
                        venta_auxiliar = venta.toJSON()
                        if (venta_auxiliar['pendiente_cobro']>=1):
                            data.append(venta_auxiliar)
                else:
                    for venta in ventas:
                        data.append(venta.toJSON())
            elif request.POST['action'] == 'anular_factura':
                id=request.POST['id']
                detalles = DetalleVenta.objects.filter(venta_id=id)
                for det in detalles:
                    tela= Tela.objects.get(id=det.tela.id)
                    tela.metraje += det.metraje_vendido
                    tela.save()
                venta = Venta.objects.get(id=id) 
                venta.anulado = True
                venta.save()
                caja = Caja.objects.get(estado=True)
                cobro = Cobro.objects.get(caja_id=id)
                if (venta.medio_cobro=='Cheque'):
                    caja.monto_cheque -= venta.monto_total
                    caja.monto_actual -= venta.monto_total
                    caja.save()

                if (venta.medio_cobro=='Efectivo'):
                    caja.monto_efectivo -= venta.monto_total
                    caja.monto_actual -= venta.monto_total
                    caja.save()
            elif request.POST['action'] == 'edit_cuota':
                estado=request.POST['estado'] 
                medio_cobro = (request.POST['medio_cobro'] )
                banco = (request.POST['banco'] )
                cuota_id=request.POST['id'] 
                cuota=CuotaVenta.objects.get(id=cuota_id)
                caja = Caja.objects.get(estado=True)
                cuota.estado =  True
                cuota.fecha_cancelacion = datetime.now()
                cuota.save()

                cobro = Cobro()
                cobro.venta_id = cuota.venta_id
                cobro.cuota_id = cuota_id
                cobro.caja_id = caja.id
                cobro.fecha_cobro = cuota.fecha_cancelacion
                cobro.medio_cobro = medio_cobro
                cobro.user_created_id = self.request.user.id
                if (medio_cobro=='Cheque'):
                    cobro.monto_cobrado = cuota.monto_cuota
                    cobro.banco_id = banco
                    caja.monto_cheque += cobro.monto_cobrado
                    caja.monto_actual += cobro.monto_cobrado

                else:
                    cobro.monto_cobrado = cuota.monto_cuota
                    caja.monto_efectivo += cobro.monto_cobrado
                    caja.monto_actual += cobro.monto_cobrado
                caja.save()
                cobro.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

class VentaCobro(LoginRequiredMixin, generic.ListView):
    model = CuotaVenta 
    template_name = "ventas/ventas_cobro_list.html"
    login_url = 'bases:login'

    def queryset(self):

        fecha_desde = str(self.request.POST['fecha_desde'])
        fecha_desde = datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_hasta = str(self.request.POST['fecha_hasta'])
        fecha_hasta = datetime.strptime(fecha_hasta, "%d/%m/%Y").strftime("%Y-%m-%d")

        deudas = CuotaVenta.objects.select_related('venta').filter(fecha_vencimiento__range=(fecha_desde,fecha_hasta))
        deudas = deudas.filter(venta__anulado = False, estado=False)
        cliente = self.request.POST['cliente']
        if cliente:
            deudas = deudas.filter(Q(venta__cliente_razon_social__icontains=cliente)| Q(venta__nro_factura__icontains=cliente))
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


class VentaCreate(LoginRequiredMixin, generic.CreateView):
    model=Venta
    form_class=VentaForm
    template_name="ventas/venta_form.html"
    success_url=reverse_lazy("ventas:ventas_list")
    login_url="bases:login"

    def render_to_response(self, context, **response_kwargs):
        configuracion_venta = ConfiguracionVenta.objects.filter(estado=True).first()
        if (not configuracion_venta): 
            messages.info(self.request, 'No existe configuración del Timbrado. Por favor configurelo')
            return HttpResponseRedirect(reverse_lazy('ventas:ventas_list'))
        
        if (configuracion_venta.fecha_inicio_timbrado <= date.today() and date.today()<=configuracion_venta.fecha_fin_timbrado): 
            pass
        else:
            messages.info(self.request, 'La fecha del timbrado ha expirado. Por favor configure un nuevo timbrado.')
            return HttpResponseRedirect(reverse_lazy('ventas:ventas_list'))
        
        caja = Caja.objects.filter(estado=True).first()
        if (caja): 
            pass
        else:
            messages.error(self.request, 'No existe una caja para operar. Por favor abra la caja para vender.')
            return HttpResponseRedirect(reverse_lazy('ventas:ventas_list'))

        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        configuracion_venta = ConfiguracionVenta.objects.filter(estado=True).first()
        if (not configuracion_venta): 
            messages.info(self.request, 'No existe configuración del Timbrado. Por favor configurelo')
            return HttpResponseRedirect(reverse_lazy('ventas:ventas_list'))
        caja = Caja.objects.filter(estado=True).first()
        #user = caja.user_created_id
        context ["bancos"] = Banco.objects.filter(estado=True)
        numero = str(configuracion_venta.numero)
        cantidad_digito = 7 - len(numero)
        prefijo = '0' * cantidad_digito
        context['numero_factura'] = '00'+str(configuracion_venta.rubro)+'-00'+str(configuracion_venta.sucursal)+'-'+prefijo+''+str(configuracion_venta.numero)
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
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']), metraje__gt=0, estado=True)
                telas_oferta = TelaOferta.objects.select_related('tela').filter(Q(tela__codigo__icontains=request.POST['term']) | Q(tela__nombre__icontains=request.POST['term']), metraje_oferta__gt=0, estado=True)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo + ' MET: ' + str(tela.metraje)
                    data.append(item)

                for tela_oferta in telas_oferta:
                    aux = tela_oferta.toJSON()
                    aux['text'] = 'TELA: '+ tela_oferta.tela.nombre + ' '+ tela_oferta.descripcion + ' COD: ' + tela_oferta.tela.codigo + ' MET: ' + str(tela_oferta.metraje_oferta)
                    data.append(aux)
            elif action == 'add':
                request_venta = json.loads(request.POST['venta'])
                print(request_venta)
                with transaction.atomic():
                    venta = Venta()
                    cliente = Cliente.objects.get(pk=request_venta['cliente'])
                    venta.nro_factura = request_venta['numero_factura']
                    venta.cliente_id = request_venta['cliente']
                    venta.cliente_razon_social = cliente.razon_social
                    venta.fecha_venta = str(request_venta['fecha_venta'])
                    venta.fecha_venta = datetime.strptime(venta.fecha_venta, "%d/%m/%Y").strftime("%Y-%m-%d")
                    venta.condicion_venta = request_venta['condicion_venta']
                    venta.medio_cobro = request_venta['medio_cobro']
                    venta.user_created_id = self.request.user.id
                    venta.plazo = request_venta['plazo']
                    venta.numero_cheque = request_venta['numero_cheque']
                    print(request_venta['numero_cheque'])
                    print(venta.numero_cheque)
                    venta.save()
                    
                    monto_total = 0
                    #sub_total_sin_iva = 0
                    total_iva_10 = 0
                    for det in request_venta['telas']:
                        detalle =  DetalleVenta()
                        detalle.venta_id = venta.id
                        tela_id = det['id']
                        if (det['oferta'] == 1):
                            detalle.descripcion = det['nombre'] + ' ' +det['descripcion']
                            tela_id = det['tela_id']
                        else:
                            detalle.descripcion = det['nombre']
                        detalle.tela_id = tela_id
                        detalle.metraje_vendido = float(det['metraje_vendido'])
                        detalle.precio_unitario = int(det['precio_venta'])
                        detalle.sub_total = round(float(det['metraje_vendido']) * int(det['precio_venta']))
                        #sub_total_sin_iva += detalle.sub_total
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        #tela = Tela.objects.get(pk=detalle.tela_id)
                        #tela.metraje -=  detalle.metraje_vendido
                        #tela.save()
                        detalle.save()

                        if (det['oferta'] == 1):
                            tela_oferta = TelaOferta.objects.get(estado=True, id = det['id'] )
                            tela_oferta.metraje_oferta -= detalle.metraje_vendido
                            tela_oferta.save()
                        
                        else:
                            tela = Tela.objects.get(pk=detalle.tela_id)
                            tela.metraje -=  detalle.metraje_vendido
                            tela.save()

                        '''    
                        if (det['oferta'] == 1):
                            tela_oferta = TelaOferta.objects.get(estado=True, tela_id = detalle.tela_id )
                            tela_oferta.metraje_oferta -= detalle.metraje_vendido
                            if (tela_oferta.metraje_oferta == 0):
                                tela_oferta.estado = False
                            tela_oferta.save()
                        '''
                    data = {'id': venta.id}
                    #venta.sub_total_sin_iva = sub_total_sin_iva
                    venta.monto_total = monto_total
                    venta.total_iva_10 = total_iva_10
                    venta.save()



                    caja = Caja.objects.get(estado=True)
                    #if (venta.medio_cobro=='Cheque'):
                    #    caja.monto_cheque += venta.monto_total
                    #    caja.save()

                    #if (venta.medio_cobro=='Efectivo'):
                    #    caja.monto_efectivo += venta.monto_total
                    #    caja.monto_actual += caja.monto_efectivo
                    #    caja.save()

                    if (venta.condicion_venta=='contado'):
                        cobro = Cobro()
                        cobro.venta_id = venta.id
                        cobro.caja_id = caja.id
                        cobro.monto_cobrado = venta.monto_total
                        cobro.medio_cobro = venta.medio_cobro
                        cobro.user_created_id = self.request.user.id
                        cobro.fecha_cobro = venta.fecha_venta
                        if (cobro.medio_cobro=='Efectivo'):
                            caja.monto_efectivo += venta.monto_total
                            caja.monto_actual += venta.monto_total
                        if (cobro.medio_cobro=='Cheque'):
                            nombre_banco = Banco.objects.get(pk=request_venta['banco'])                    
                            cobro.banco = nombre_banco
                            caja.monto_cheque += venta.monto_total
                            caja.monto_actual += venta.monto_total
                            cobro.numero_cheque = venta.numero_cheque
                        cobro.save()
                        caja.save()

                    if (venta.condicion_venta=='credito'):
                        venta.plazo = request_venta['plazo']
                        cantidad = int(int(venta.plazo)/30)
                        monto = int(int(venta.monto_total)/cantidad)
                        for i in range(cantidad):
                            deuda = CuotaVenta()
                            deuda.venta_id = venta.id
                            deuda.numero_cuota = i+1
                            deuda.monto_cuota = monto
                            deuda.fecha_vencimiento =  datetime.now() + relativedelta(months=i+1)
                            deuda.user_created_id = self.request.user.id
                            deuda.estado = False
                            deuda.save()

                    configuracion = ConfiguracionVenta.objects.filter(estado=True).first()
                    configuracion.numero += 1
                    configuracion.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class VentaEdit(LoginRequiredMixin, generic.CreateView):
    model=Venta
    form_class=VentaForm
    template_name="ventas/venta_form.html"
    success_url=reverse_lazy("ventas:ventas_list")
    login_url="bases:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        configuracion_venta = ConfiguracionVenta.objects.filter(estado=True).first()
        print ((date.today()>configuracion_venta.fecha_fin_timbrado))
        print (date.today())
        context ["bancos"] = Banco.objects.all()
        numero = str(configuracion_venta.numero)
        cantidad_digito = 7 - len(numero)
        prefijo = '0' * cantidad_digito
        context['numero_factura'] = '00'+str(configuracion_venta.rubro)+'-00'+str(configuracion_venta.sucursal)+'-'+prefijo+''+str(configuracion_venta.numero)
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
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']) | Q(nombre__icontains=request.POST['term']), metraje__gt=0)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo + ' MET: ' + str(tela.metraje)
                    data.append(item)
            elif action == 'edit':
                request_venta = json.loads(request.POST['venta'])
                with transaction.atomic():
                    venta = Venta.objects.get(id=self.get_object().id)
                    cliente = Cliente.objects.get(pk=request_venta['cliente'])
                    venta.nro_factura = request_venta['numero_factura']
                    venta.cliente_id = request_venta['cliente']
                    venta.cliente_razon_social = cliente.razon_social
                    venta.fecha_venta = str(request_venta['fecha_venta'])
                    venta.fecha_venta = datetime.strptime(venta.fecha_venta, "%d/%m/%Y").strftime("%Y-%m-%d")
                    venta.condicion_venta = request_venta['condicion_venta']
                    venta.user_created_id = self.request.user.id
                    venta.plazo = request_venta['plazo']
                    venta.save()
                    
                    monto_total = 0
                    #sub_total_sin_iva = 0
                    total_iva_10 = 0
                    for det in request_venta['telas']:
                        detalle =  DetalleVenta()
                        detalle.venta_id = venta.id
                        detalle.tela_id = det['id']
                        detalle.metraje_vendido = float(det['metraje_vendido'])
                        detalle.precio_unitario = int(det['precio_venta'])
                        detalle.sub_total = float(det['metraje_vendido']) * int(det['precio_venta'])
                        #sub_total_sin_iva += detalle.sub_total
                        detalle.sub_total_iva_10 =  round(detalle.sub_total / 11)
                        monto_total += detalle.sub_total
                        total_iva_10 += detalle.sub_total_iva_10
                        detalle.user_created_id = self.request.user.id
                        tela = Tela.objects.get(pk=detalle.tela_id)
                        tela.metraje -=  detalle.metraje_vendido
                        tela.save()
                        detalle.save()
                    
                    data = {'id': venta.id}
                    #venta.sub_total_sin_iva = sub_total_sin_iva
                    venta.monto_total = monto_total
                    venta.total_iva_10 = total_iva_10
                    venta.save()

                    if (venta.condicion_venta=='credito'):
                        venta.plazo = request_venta['plazo']
                        cantidad = int(int(venta.plazo)/30)
                        monto = int(int(venta.monto_total)/cantidad)
                        for i in range(cantidad):
                            print(i)
                            deuda = CuotaVenta()
                            deuda.venta_id = venta.id
                            deuda.numero_cuota = i+1
                            deuda.monto_cuota = monto
                            deuda.fecha_vencimiento =  datetime.now() + relativedelta(months=i+1)
                            deuda.user_created_id = self.request.user.id
                            deuda.estado = False
                            deuda.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class VentaListadoPdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            template = get_template('ventas/listado_pdf.html')
            context = {
                'ventas': Venta.objects.get(pk=self.kwargs['pk']),
                #'cobros': Cobro.objects.select_related('venta').filter(venta_id=self.kwargs['pk'])
            }
            print(context)
            print(self.kwargs['pk'])

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('ventas:ventas_list'))

        