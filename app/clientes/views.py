
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

from .models import Cliente
from .forms import ClienteForm
from ubicaciones.models import Ciudad

class ClienteView(LoginRequiredMixin,generic.ListView):
    model = Cliente 
    template_name = "clientes/cliente_list.html"
    #context_object_name = "obj"
    login_url = 'bases:login'


class ClienteList(LoginRequiredMixin,generic.ListView):
    model = Cliente 
    login_url = 'bases:login'

    def get_queryset(self):
        estado = int(self.request.GET.get('estado'))
        clientes = self.model.objects.filter(estado=estado).values(
                            'id','nombre_cliente','cedula','ruc','nro_celular','estado')
        buscar_cliente = self.request.GET.get('cliente')

        if estado:
            print(estado)
            clientes = clientes.filter(estado=estado)
        if buscar_cliente:
            clientes = clientes.filter(Q(nombre_cliente__icontains=buscar_cliente) |
                Q(cedula__icontains=buscar_cliente) | Q(ruc__icontains=buscar_cliente))

        return clientes
        

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            inicio = int(request.GET.get('inicio'))
            fin = int(request.GET.get('limite'))
            clientes = self.get_queryset()
            list_data = []
            for indice, valor in enumerate (clientes[inicio:inicio+fin],inicio):
                list_data.append(valor)

            data = {
                'length': clientes.count(),
                'objects': list_data
            }
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            return redirect("clientes:cliente_list")


class ClienteNew(LoginRequiredMixin, generic.CreateView):
    model=Cliente
    template_name="clientes/cliente_form.html"
    context_object_name="obj"
    form_class=ClienteForm
    success_url=reverse_lazy("clientes:cliente_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        context = super(ClienteNew,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        return context

class ClienteEdit(LoginRequiredMixin, generic.UpdateView):
    model=Cliente
    template_name="clientes/cliente_form.html"
    context_object_name="obj"
    form_class=ClienteForm
    success_url=reverse_lazy("clientes:cliente_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ClienteEdit,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        context ["obj"] = Cliente.objects.filter(pk=pk).first()
        return context

def cliente_eliminar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()
    if request.method=='GET':
        try:
            cliente.delete()
            messages.success(request, "Registro eliminado correctamente." )
        except ProtectedError:
            messages.error(request, "No se puede eliminar el registro" )
        return redirect("clientes:cliente_list")


def cliente_inactivar (request,id):
    template_name = 'base/modal_eliminar.html'
    contexto={}
    cli= Cliente.objects.filter(pk=id).first()

    if not cli:
        return HttpResponse('Cliente Inactivado')
    
    if request.method=='GET':
        contexto={'obj':cli}

    if request.method=='POST':
        cli.estado=False
        cli.save()
        contexto={'obj':'OK'}
        return HttpResponse('Cliente Inactivado')
    
    return render(request, template_name, contexto)