from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import generic
from datetime import datetime
from telas.models import Tela
from ventas.models import Venta, CuotaVenta
from compras.models import Compra
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url = 'bases:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_disponible = Tela.objects.filter(fecha_eliminacion__isnull=True).count()
        
        today = datetime.now()
        year = today.year
        month = today.month

        if (month == 1) :
            past_month = 12
            past_year = year - 1
        else:
            past_month = today.month - 1
            past_year = year

        venta_mes_anterior = Venta.objects.filter(fecha_venta__year=past_year, fecha_venta__month = past_month).aggregate(
                    r=Coalesce(Sum('monto_total'), 0)).get('r')

        venta_mes_actual = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month = month).aggregate(
                    r=Coalesce(Sum('monto_total'), 0)).get('r')

        compra_mes_anterior = Compra.objects.filter(fecha_compra__year=past_year, fecha_compra__month = past_month).aggregate(
                    r=Coalesce(Sum('monto_total'), 0)).get('r')

        compra_mes_actual = Compra.objects.filter(fecha_compra__year=year, fecha_compra__month = month).aggregate(
                    r=Coalesce(Sum('monto_total'), 0)).get('r')

        if (venta_mes_anterior <= 0 and venta_mes_actual <= 0):
            nivel_venta = 0.00
        elif (venta_mes_anterior <= 0 and venta_mes_actual > 0):
            porcentaje_venta = ( int(venta_mes_actual) / int(venta_mes_actual)) * 100
            nivel_venta = round (porcentaje_venta, 2)
        else:
            porcentaje_venta = ( int(venta_mes_actual) - int(venta_mes_anterior) ) / int(venta_mes_anterior) * 100
            nivel_venta = round (porcentaje_venta, 2)

        if (compra_mes_anterior <= 0 and compra_mes_actual <= 0):
            nivel_compra = 0.00
        elif (compra_mes_anterior <= 0 and compra_mes_actual > 0):
            porcentaje_compra = ( int(compra_mes_actual) / int(compra_mes_actual) ) * 100
            nivel_compra = round (porcentaje_compra, 2)
        else:
            porcentaje_compra = ( int(compra_mes_actual) - int(compra_mes_anterior) ) / int(compra_mes_anterior) * 100
            nivel_compra = round (porcentaje_compra, 2)

        clientes_adeudores = Venta.objects.filter(cuotaventa__estado=False,
                            cuotaventa__fecha_vencimiento__year=year, 
                            cuotaventa__fecha_vencimiento__month = month).annotate(
                                dcount=Count('cliente_id')
                            ).count()
        

        context["stock_disponible"] = stock_disponible
        context["venta_mes_actual"] = venta_mes_actual
        context["compra_mes_actual"] = compra_mes_actual
        context["nivel_venta"] = nivel_venta
        context["nivel_compra"] = nivel_compra
        context["clientes_adeudores"] = clientes_adeudores
        return context
    


class LoginFormView(LoginView):
    template_name = 'bases/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bases:home')
        return super().dispatch(request, *args, **kwargs)
