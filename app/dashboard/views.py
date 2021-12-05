from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from ventas.models import Venta, DetalleVenta
from telas.models import Tela
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'dash_ventas_mes':
                data = self.get_obtener_ventas_por_mes()
            elif action == 'dash_ventas_productos_anho_mes':
                data = {
                    'name' : 'Porcentaje',
                    'colorByPoint' : True,
                    'data' : self.obtener_ventas_productos_por_anho_mes()
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = 'Ocurrió un error inesperado. Por favor comuníquese con soporte'
        return JsonResponse(data, safe=False)

    def get_obtener_ventas_por_mes(self):
        data = []
        try:
            year = self.request.POST['year'] if (self.request.POST['year']) else datetime.now().year
            for month in range (1,13):
                total = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month = month).aggregate(r=Coalesce(Sum('monto_total'), 0)).get('r')
                data.append(int(total))
        except:
            pass
        return data

    def obtener_ventas_productos_por_anho_mes(self):
        data = []
        year = self.request.POST['year'] if (self.request.POST['year']) else datetime.now().year
        month = self.request.POST['month'] if (self.request.POST['month']) else datetime.now().month
        #year = datetime.now().year
        #month = datetime.now().month
        try:
            telas = Tela.objects.all()
            for tela in telas:
                total = DetalleVenta.objects.filter(venta__fecha_venta__year=year, venta__fecha_venta__month = month, tela_id = tela.id).aggregate(
                    r=Coalesce(Sum('sub_total'), 0)).get('r')
                if (total > 0):
                    data.append({
                        'name' : tela.nombre,
                        'y' : int(total)
                    })
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = datetime.now().year
        month = datetime.now().month
        context["reportes_ventas"] =  self.get_obtener_ventas_por_mes()
        context["year"] =  year
        context["mes"] =  str(month)
        meses = {
            "1" : "ENERO",
            "2" : "FEBRERO",
            "3" : "MARZO",
            "4" : "ABRIL",
            "5" : "MAYO",
            "6" : "JUNIO",
            "7" : "JULIO",
            "8" : "AGOSTO",
            "9" : "SEPTIEMBRE",
            "10" : "OCTUBRE",
            "11" : "NOVIEMBRE",
            "12" : "DICIEMBRE"
        }
        context['meses'] = meses
        return context
    
