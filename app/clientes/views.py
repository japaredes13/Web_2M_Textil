
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from datetime import datetime

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


class ClienteCreate(LoginRequiredMixin, generic.CreateView):
    model=Cliente
    template_name="clientes/cliente_form.html"
    context_object_name="obj"
    form_class=ClienteForm
    success_url=reverse_lazy("clientes:cliente_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Cliente registrado éxitosamente.')
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        context = super(ClienteCreate,self).get_context_data(**kwargs)
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
        messages.success(self.request, 'Cliente modificado éxitosamente.')
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ClienteEdit,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        context ["obj"] = Cliente.objects.filter(pk=pk).first()
        return context

def cliente_delete(request,id):
    try:
        cliente= Cliente.objects.get(pk=id)
        cliente.fecha_eliminacion = datetime.now()
        cliente.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Cliente.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)