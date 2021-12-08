from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from bases.mixins import ValidatePermissionRequired
from .models import  ConfiguracionUsuario, ConfiguracionProducto, ConfiguracionVenta, ConfiguracionEgreso
from .forms import ConfiguracionUsuarioForm, ConfiguracionProductoForm, ConfiguracionVentaForm, ConfiguracionEgresoForm
from datetime import datetime, date

class ConfiguracionUsuarioView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    paginate_by = 6
    permission_required = 'configuracion.view_configuracionusuario'
    template_name = "configuracion/configuracion_usuario_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionUsuario.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionUsuarioEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=ConfiguracionUsuario
    permission_required = 'configuracion.change_configuracionusuario'
    template_name="configuracion/configuracion_usuario_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionUsuarioForm
    success_url= reverse_lazy("configuracion:configuracion_usuario_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

class ConfiguracionProductoView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    paginate_by = 6
    permission_required = 'configuracion.view_configuracionproducto'
    template_name = "configuracion/configuracion_producto_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionProducto.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionProductoEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=ConfiguracionProducto
    permission_required = 'configuracion.change_configuracionproducto'
    template_name="configuracion/configuracion_producto_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionProductoForm
    success_url= reverse_lazy("configuracion:configuracion_producto_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class ConfiguracionVentaView(LoginRequiredMixin, ValidatePermissionRequired,generic.ListView):
    paginate_by = 6
    permission_required = 'configuracion.view_configuracionventa'
    template_name = "configuracion/configuracion_venta_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha_hoy"] = datetime.now().strftime('%Y-%m-%d')
        return context
    

    def get_queryset(self):
        queryset = ConfiguracionVenta.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionVentaCreate(LoginRequiredMixin,ValidatePermissionRequired, generic.CreateView):
    model = ConfiguracionVenta
    permission_required = 'configuracion.add_configuracionventa'
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

class ConfiguracionVentaEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=ConfiguracionVenta
    permission_required = 'configuracion.change_configuracionventa'
    template_name="configuracion/configuracion_venta_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionVentaForm
    success_url= reverse_lazy("configuracion:configuracion_venta_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)

class ConfiguracionEgresoView(LoginRequiredMixin,ValidatePermissionRequired, generic.ListView):
    paginate_by = 6
    permission_required = 'configuracion.view_configuracionegreso'
    template_name = "configuracion/configuracion_egreso_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = ConfiguracionEgreso.objects.filter(fecha_eliminacion__isnull=True)
        return queryset

class ConfiguracionEgresoEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=ConfiguracionEgreso
    permission_required = 'configuracion.change_configuracionegreso'
    template_name="configuracion/configuracion_egreso_form.html"
    context_object_name = 'obj'
    form_class=ConfiguracionEgresoForm
    success_url= reverse_lazy("configuracion:configuracion_egreso_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)