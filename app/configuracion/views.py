from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ConfiguracionUsuario
from .forms import ConfiguracionUsuarioForm

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