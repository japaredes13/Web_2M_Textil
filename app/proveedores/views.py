from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from bases.mixins import ValidatePermissionRequired
from django.http import HttpResponse, JsonResponse, response
from datetime import datetime
from .models import Proveedor
from .forms import ProveedorForm
from ubicaciones.models import Ciudad


class ProveedorView(LoginRequiredMixin,ValidatePermissionRequired,generic.ListView):
    model = Proveedor 
    permission_requied = 'proveedores.view_proveedor'
    template_name = "proveedores/proveedor_list.html"
    login_url = 'bases:login'
    
    def queryset(self):
        proveedores = Proveedor.objects.filter(fecha_eliminacion__isnull=True)
        proveedor = self.request.POST['proveedor']
        if proveedor:
            proveedores = proveedores.filter(Q(nombre_empresa__icontains=proveedor) | Q(ruc__icontains=proveedor))
        return proveedores


    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                proveedores = self.queryset()
                for proveedor in proveedores:
                    data.append(proveedor.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)


class ProveedorCreate(LoginRequiredMixin,ValidatePermissionRequired, generic.CreateView):
    model=Proveedor
    permission_required = 'proveedores.add_proveedor'
    template_name="proveedores/proveedor_form.html"
    context_object_name="obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("proveedores:proveedor_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, 'Proveedor registrado éxitosamente.')
        return super().form_valid(form)


    def get_context_data (self, **kwargs):
        context = super(ProveedorCreate,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        return context


class ProveedorEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=Proveedor
    permission_required = 'proveedores.change_proveedor'
    template_name="proveedores/proveedor_form.html"
    context_object_name="obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("proveedores:proveedor_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id
        messages.success(self.request, 'Proveedor modificado éxitosamente.')
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(ProveedorEdit,self).get_context_data(**kwargs)
        context ["ciudades"] = Ciudad.objects.all()
        context ["obj"] = Proveedor.objects.filter(pk=pk).first()
        return context

def proveedor_delete(request,id):
    try:
        proveedor= Proveedor.objects.get(pk=id)
        proveedor.fecha_eliminacion = datetime.now()
        proveedor.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Proveedor.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)

def search_ruc(request):
    ruc = request.GET.get('ruc')
    proveedor = Proveedor.objects.get(ruc = ruc)
    print(proveedor)
    if proveedor:
        data = {
            'existe':True,
            'message':'El campo ruc ya existe'
        }
    else:
        data = {
            'existe':False,
            'message':''
        }
    return JsonResponse(data, safe=False)
