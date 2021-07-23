from django.http.response import JsonResponse
from .models import Venta, DetalleVenta
from .forms import VentaForm
from telas.models import Tela
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


class VentaView(LoginRequiredMixin, generic.CreateView):
    model = Venta 
    fields = '__all__'
    template_name = "ventas/ventas_list.html"
    login_url = 'bases:login'

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
                    item['value'] = tela.nombre
                    data.append(item)
            elif action == 'add':
                request_venta = json.loads(request.POST['venta'])
                print (request_venta)
                '''
                venta = new Venta()
                venta.cliente_id = request_venta['cliente_id']
                venta.fecha_venta = request_venta['fecha_venta]
                venta.condicion_venta = request_venta['condicion_venta]
                venta.save()

                for det in request_venta['detalles']
                    detalle = DetalleVenta()
                    detalle.venta_id = venta.id
                    detalle.tela_id = det['id']
                    detalle.metraje_vendido = det['metraje_vendido']
                    detalle.precio_unitario = det['precio']
                    detalle.sub_total = calcular
                    detalle.sub_total_iva_10 = calcular

                venta.
                '''
            else:
                data['error'] = 'No hay nada'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)