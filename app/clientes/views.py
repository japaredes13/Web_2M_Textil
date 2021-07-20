
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
import json

from .models import Cliente
from .forms import ClienteForm
from ubicaciones.models import Ciudad

class ClienteView(LoginRequiredMixin,generic.ListView):
    model = Cliente 
    template_name = "clientes/cliente_list.html"
    login_url = 'bases:login'

    def queryset(self):
        estado = int(self.request.POST['estado'])
        clientes = Cliente.objects.filter(estado=estado, fecha_eliminacion__isnull=True)
        buscar_cliente = self.request.POST['cliente']
        if buscar_cliente:
            clientes = clientes.filter(Q(nombre_cliente__icontains=buscar_cliente) |
                Q(cedula__icontains=buscar_cliente) | Q(ruc__icontains=buscar_cliente))
        return clientes


    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                clientes = self.queryset()
                for cliente in clientes:
                    data.append(cliente.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)


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