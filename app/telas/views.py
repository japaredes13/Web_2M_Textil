
from django.http.response import HttpResponse, HttpResponseRedirect
from tipos.models import Categoria
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tela
from .forms import TelaForm
from datetime import datetime

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class TelaList(LoginRequiredMixin,generic.ListView):
    model = Tela 
    template_name = "telas/tela_list.html"
    login_url = 'bases:login'

    def queryset(self):
        telas = Tela.objects.filter(fecha_eliminacion__isnull=True).order_by('nombre')
        buscar_tela = self.request.POST['tela']
        categoria = self.request.POST['categoria']
        if categoria:
            telas = telas.filter(categoria=categoria)
        if buscar_tela:
            telas = telas.filter(Q(codigo__icontains=buscar_tela) | Q(nombre__icontains=buscar_tela))
        return telas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(fecha_eliminacion__isnull=True)
        return context


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
        messages.success(self.request, "Tela registrada éxitosamente." )
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
        messages.success(self.request, "Tela modificada éxitosamente." )
        return super().form_valid(form)


def tela_delete(request,id):
    try:
        tela= Tela.objects.get(pk=id)
        tela.fecha_eliminacion = datetime.now()
        tela.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Tela.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)


class TelaInvoicePdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            print(request.GET)
            template = get_template('telas/listado_pdf.html')
            context = {
                'telas':Tela.objects.all()
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('telas:telas_list'))






 