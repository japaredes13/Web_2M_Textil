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

class DepartamentoView(LoginRequiredMixin, generic.ListView):
    model = Departamento
    template_name = "ubicaciones/departamentos/departamento_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class DepartamentoNew(LoginRequiredMixin,
                   generic.CreateView):
    model=Departamento
    template_name="ubicaciones/departamento_form.html"
    context_object_name = 'obj'
    form_class=DepartamentoForm
    success_url= reverse_lazy("ubicaciones:departamento_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        return super().form_valid(form)
    

class DepartamentoEdit(LoginRequiredMixin,
                   generic.UpdateView):
    model=Departamento
    template_name="ubicaciones/departamento_form.html"
    context_object_name = 'obj'
    form_class=DepartamentoForm
    success_url= reverse_lazy("ubicaciones:departamento_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id
        return super().form_valid(form)
    

def departamento_eliminar(request,id):
    dpto= Departamento.objects.filter(pk=id).first()
    print(dpto)
    if request.method=='GET':
        try:
            dpto.delete()
            messages.success(request, "Registro eliminado correctamente." )
        except ProtectedError:
            messages.error(request, "No se puede eliminar el registro" )
        return redirect("ubicaciones:departamento_list")



def departamento_inactivar(request, id):
    dpto= Departamento.objects.filter(pk=id).first()
    contexto={}
    template_name="base/modal_eliminar.html"

    if not dpto:
        return redirect("ubicaciones:departamento_list")
    
    if request.method=='GET':
        contexto={'obj':dpto}
    
    if request.method=='POST':
        dpto.estado=False
        dpto.save()
        return redirect("ubicaciones:departamento_list")

    return render(request,template_name,contexto)

class CiudadView(LoginRequiredMixin, generic.ListView):
    model = Ciudad
    template_name = "ubicaciones/ciudad_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class CiudadNew(LoginRequiredMixin,
                   generic.CreateView):
    model=Ciudad
    template_name="ubicaciones/ciudad_form.html"
    context_object_name = 'obj'
    form_class=CiudadForm
    success_url= reverse_lazy("ubicaciones:ciudad_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        return super().form_valid(form)
    

class CiudadEdit(LoginRequiredMixin,
                   generic.UpdateView):
    model=Ciudad
    template_name="ubicaciones/ciudad_form.html"
    context_object_name = 'obj'
    form_class=CiudadForm
    success_url= reverse_lazy("ubicaciones:ciudad_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id
        return super().form_valid(form)
    
def ciudad_eliminar(request,id):
    ciudad= Ciudad.objects.filter(pk=id).first()
    print(ciudad)
    if request.method=='GET':
        try:
            ciudad.delete()
            messages.success(request, "Registro eliminado correctamente." )
        except ProtectedError:
            messages.error(request, "No se puede eliminar el registro" )
        return redirect("ubicaciones:ciudad_list")


def ciudad_inactivar(request, id):
    dpto= Ciudad.objects.filter(pk=id).first()
    contexto={}
    template_name="base/modal_eliminar.html"

    if not dpto:
        return redirect("ubicaciones:ciudad_list")
    
    if request.method=='GET':
        contexto={'obj':dpto}
    
    if request.method=='POST':
        dpto.estado=False
        dpto.save()
        return redirect("ubicaciones:ciudad_list")

    return render(request,template_name,contexto)


def ciudades_ajax(request):
    if request.is_ajax():
        term = request.GET.get('term')
        ciudades = Ciudad.objects.values('id','descripcion').filter(descripcion__icontains=term)
        response_content = list(ciudades.values())
        return HttpResponse(json.dumps(response_content), 'application/json')