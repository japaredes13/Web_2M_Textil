from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.db.models import ProtectedError 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from .models import Departamento, Ciudad
from .forms import DepartamentoForm, CiudadForm
from datetime import datetime

class DepartamentoView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "ubicaciones/departamentos/departamento_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = Departamento.objects.filter(fecha_eliminacion__isnull=True).order_by('descripcion')
        return queryset


class DepartamentoCreate(LoginRequiredMixin, generic.CreateView):
    model = Departamento
    template_name="ubicaciones/departamentos/departamento_form.html"
    context_object_name = 'obj'
    form_class=DepartamentoForm
    success_url= reverse_lazy("ubicaciones:departamento_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class DepartamentoEdit(LoginRequiredMixin, generic.UpdateView):
    model=Departamento
    template_name="ubicaciones/departamentos/departamento_form.html"
    context_object_name = 'obj'
    form_class=DepartamentoForm
    success_url= reverse_lazy("ubicaciones:departamento_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

def departamento_delete(request,id):
    try:
        departamento= Departamento.objects.get(pk=id)
        departamento.fecha_eliminacion = datetime.now()
        departamento.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Departamento.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)


class CiudadView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "ubicaciones/ciudades/ciudad_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = Ciudad.objects.filter(fecha_eliminacion__isnull=True).order_by('descripcion')
        return queryset


class CiudadCreate(LoginRequiredMixin, generic.CreateView):
    model=Ciudad
    template_name="ubicaciones/ciudades/ciudad_form.html"
    context_object_name = 'obj'
    form_class=CiudadForm
    success_url= reverse_lazy("ubicaciones:ciudad_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class CiudadEdit(LoginRequiredMixin, generic.UpdateView):
    model=Ciudad
    template_name="ubicaciones/ciudades/ciudad_form.html"
    context_object_name = 'obj'
    form_class=CiudadForm
    success_url= reverse_lazy("ubicaciones:ciudad_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id
        messages.success(self.request, "Registro eliminado correctamente." )
        return super().form_valid(form)
    
def ciudad_delete(request,id):
    try:
        ciudad= Ciudad.objects.get(pk=id)
        ciudad.fecha_eliminacion = datetime.now()
        ciudad.save() 
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Ciudad.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)



def ciudades_ajax(request):
    if request.is_ajax():
        term = request.GET.get('term')
        ciudades = Ciudad.objects.values('id','descripcion').filter(descripcion__icontains=term)
        response_content = list(ciudades.values())
        return HttpResponse(json.dumps(response_content), 'application/json')