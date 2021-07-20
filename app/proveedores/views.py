from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

from .models import Proveedor
from .forms import ProveedorForm
from ubicaciones.models import Ciudad


class ProveedorView(LoginRequiredMixin,generic.ListView):
    model = Proveedor 
    template_name = "proveedores/proveedor_list.html"
    #context_object_name = "obj"
    login_url = 'bases:login'


class ProveedorList(LoginRequiredMixin,generic.ListView):
    model = Proveedor
    login_url = 'bases:login'

    def get_queryset(self):
        estado = int(self.request.GET.get('estado'))
        proveedores = self.model.objects.filter(estado=estado).values(
                            'id','nombre_empresa','ruc','email','nro_celular','direccion','estado')
        buscar_proveedor = self.request.GET.get('proveedor')

        if estado:
            print(estado)
            proveedores = proveedores.filter(estado=estado)
        if buscar_proveedor:
            proveedores = proveedores.filter(Q(nombre_empresa__icontains=buscar_proveedor) |Q(ruc__icontains=buscar_proveedor))

        return proveedores
        

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            inicio = int(request.GET.get('inicio'))
            fin = int(request.GET.get('limite'))
            proveedores = self.get_queryset()
            list_data = []
            for indice, valor in enumerate (proveedores[inicio:inicio+fin],inicio):
                list_data.append(valor)

            data = {
                'length': proveedores.count(),
                'objects': list_data
            }
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            return redirect("proveedores:proveedor_list")


class ProveedorNew(LoginRequiredMixin, generic.CreateView):
    model=Proveedor
    template_name="proveedores/proveedor_form.html"
    context_object_name="obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("proveedores:proveedor_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        context = super(ProveedorNew,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        return context

class ProveedorEdit(LoginRequiredMixin, generic.UpdateView):
    model=Proveedor
    template_name="proveedores/proveedor_form.html"
    context_object_name="obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("proveedores:proveedor_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ProveedorEdit,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        context ["obj"] = Proveedor.objects.filter(pk=pk).first()
        return context

def proveedor_eliminar(request,id):
    proveedor = Proveedor.objects.filter(pk=id).first()
    if request.method=='GET':
        try:
            proveedor.delete()
            messages.success(request, "Registro eliminado correctamente." )
        except ProtectedError:
            messages.error(request, "No se puede eliminar el registro" )
        return redirect("proveedores:proveedor_list")

def proveedor_inactivar (request,id):
    template_name = 'base/modal_eliminar.html'
    contexto={}
    prv = Proveedor.objects.filter(pk=id).first()

    if not prv:
        return HttpResponse('Proveedor ya se encuentra Inactivado')
    
    if request.method=='GET':
        contexto={'obj':prv}

    if request.method=='POST':
        prv.estado=False
        prv.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivado')
    
    return render(request, template_name, contexto)