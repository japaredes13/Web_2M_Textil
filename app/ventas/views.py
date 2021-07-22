from .models import Venta
from .forms import VentaForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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