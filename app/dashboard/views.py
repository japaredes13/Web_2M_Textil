from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from ventas.models import Venta
from django.db.models import Sum
from django.db.models.functions import Coalesce

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_obtener_ventas_por_mes(self):
        data = []
        try:
            year = datetime.now().year
            for month in range (1,13):
                total = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month = month).aggregate(r=Coalesce(Sum('monto_total'), 0)).get('r')
                data.append(int(total))
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reportes_ventas"] =  self.get_obtener_ventas_por_mes()
        return context
    
