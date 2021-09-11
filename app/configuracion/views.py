from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  ConfiguracionUsuario, ConfiguracionProducto, ConfiguracionVenta
from .forms import ConfiguracionUsuarioForm, ConfiguracionProductoForm, ConfiguracionVentaForm

class ConfiguracionUsuarioView(LoginRequiredMixin, generic.ListView):
    paginate_by = 6
    template_name = "configuracion/configuracion_usuario_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionUsuario.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionUsuarioEdit(LoginRequiredMixin, generic.UpdateView):
    model=ConfiguracionUsuario
    template_name="configuracion/configuracion_usuario_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionUsuarioForm
    success_url= reverse_lazy("configuracion:configuracion_usuario_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

class ConfiguracionProductoView(LoginRequiredMixin, generic.ListView):
    paginate_by = 6
    template_name = "configuracion/configuracion_producto_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionProducto.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionProductoEdit(LoginRequiredMixin, generic.UpdateView):
    model=ConfiguracionProducto
    template_name="configuracion/configuracion_producto_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionProductoForm
    success_url= reverse_lazy("configuracion:configuracion_producto_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class ConfiguracionVentaView(LoginRequiredMixin, generic.ListView):
    paginate_by = 6
    template_name = "configuracion/configuracion_venta_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionVenta.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionVentaCreate(LoginRequiredMixin, generic.CreateView):
    model = ConfiguracionVenta
    template_name="configuracion/configuracion_venta_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionVentaForm
    success_url= reverse_lazy("configuracion:configuracion_venta_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

class ConfiguracionVentaEdit(LoginRequiredMixin, generic.UpdateView):
    model=ConfiguracionVenta
    template_name="configuracion/configuracion_venta_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionVentaForm
    success_url= reverse_lazy("configuracion:configuracion_venta_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)