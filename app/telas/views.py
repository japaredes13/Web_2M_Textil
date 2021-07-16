
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
import json
from .models import Tela
from .forms import TelaForm


class TelaList(LoginRequiredMixin,generic.ListView):
    model = Tela 
    template_name = "telas/tela_list.html"
    login_url = 'bases:login'

    def queryset(self):
        telas = Tela.objects.filter(estado=True).order_by('nombre')
        buscar_tela = self.request.POST['tela']
        categoria = self.request.POST['categoria']
        if categoria:
            telas = telas.filter(categoria=categoria)
        if buscar_tela:
            telas = telas.filter(Q(codigo__icontains=buscar_tela) | Q(nombre__icontains=buscar_tela))
        return telas


    def post(self, request, *args, **kwargs):
        data={}
        try:
            if request.POST['action'] == 'search':
                data = []
                telas = self.queryset()
                for tela in telas:
                    data.append(tela.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

class TelaCreate(LoginRequiredMixin, generic.CreateView):
    model=Tela
    template_name="telas/tela_form.html"
    context_object_name="obj"
    form_class=TelaForm
    success_url=reverse_lazy("telas:tela_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        form.instance.estado = True
        messages.success(self.request, "Registro creado correctamente." )
        return super().form_valid(form)


class TelaEdit(LoginRequiredMixin, generic.UpdateView):
    model=Tela
    template_name="telas/tela_form.html"
    context_object_name = 'obj'
    form_class=TelaForm
    success_url= reverse_lazy("telas:tela_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id
        messages.success(self.request, "Registro actualizado correctamente." )
        return super().form_valid(form)


def tela_delete(request,id):
    try:
        tela= Tela.objects.filter(pk=id).first()
        tela.estado = False
        tela.save() 
        messages.success(request, "Registro eliminado correctamente." )
    except ProtectedError:
        messages.error(request, "No se puede eliminar el registro" )
    return redirect("telas:tela_list")