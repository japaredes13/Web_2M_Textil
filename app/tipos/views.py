from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.db.models import ProtectedError 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from .models import Categoria, Disenho
from .forms import CategoriaForm, DisenhoForm
from datetime import datetime

class CategoriaView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "tipos/categorias/categoria_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = Categoria.objects.filter(fecha_eliminacion__isnull=True).order_by('descripcion')
        return queryset


class CategoriaCreate(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name="tipos/categorias/categoria_form.html"
    context_object_name = 'obj'
    form_class=CategoriaForm
    success_url= reverse_lazy("tipos:categoria_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class CategoriaEdit(LoginRequiredMixin, generic.UpdateView):
    model=Categoria
    template_name="tipos/categorias/categoria_form.html"
    context_object_name = 'obj'
    form_class=CategoriaForm
    success_url= reverse_lazy("tipos:categoria_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

def categoria_delete(request,id):
    try:
        categoria= Categoria.objects.get(pk=id)
        categoria.fecha_eliminacion = datetime.now()
        categoria.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Categoria.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)


class DisenhoView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = "tipos/disenhos/disenho_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'

    def get_queryset(self):
        queryset = Disenho.objects.filter(fecha_eliminacion__isnull=True).order_by('descripcion')
        return queryset


class DisenhoCreate(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name="tipos/disenhos/disenho_form.html"
    context_object_name = 'obj'
    form_class=DisenhoForm
    success_url= reverse_lazy("tipos:disenho_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

class DisenhoEdit(LoginRequiredMixin, generic.UpdateView):
    model=Categoria
    template_name="tipos/disenhos/disenho_form.html"
    context_object_name = 'obj'
    form_class=CategoriaForm
    success_url= reverse_lazy("tipos:disenho_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id 
        messages.success(self.request, 'Registro actualizado correctamente')
        return super().form_valid(form)
    

def disenho_delete(request,id):
    try:
        disenho= Disenho.objects.get(pk=id)
        disenho.fecha_eliminacion = datetime.now()
        disenho.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Disenho.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)