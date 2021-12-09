
from django.http.response import HttpResponse, HttpResponseRedirect
from tipos.models import Categoria, Disenho
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from bases.mixins import ValidatePermissionRequired
from django.http import JsonResponse
from .models import Tela, TelaOferta
from .forms import TelaForm, TelaOfertaForm
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
from django.db import transaction
from django.template.loader import get_template
from django.db.models import Q
import json

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class TelaList(LoginRequiredMixin,ValidatePermissionRequired,generic.ListView):
    model = Tela 
    permission_required = 'telas.view_tela'
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

class TelaCreate(LoginRequiredMixin,ValidatePermissionRequired, generic.CreateView):
    model=Tela
    permission_required = 'telas.add_tela'
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

    def get_context_data (self, **kwargs):
        context = super(TelaCreate,self).get_context_data(**kwargs)
        context ["disenhos"] = Disenho.objects.all()
        context ["categorias"] = Categoria.objects.all()
        return context


class TelaEdit(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=Tela
    permission_required = 'telas.change_tela'
    template_name="telas/tela_form.html"
    context_object_name = 'obj'
    form_class=TelaForm
    success_url= reverse_lazy("telas:tela_list")
    login_url="bases:login"

    def form_valid(self, form):
        form.instance.user_updated_id = self.request.user.id
        messages.success(self.request, "Tela modificada éxitosamente." )
        return super().form_valid(form)

    def get_context_data (self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(TelaEdit,self).get_context_data(**kwargs)
        context ["disenhos"] = Disenho.objects.all()
        context ["categorias"] = Categoria.objects.all()
        context ["obj"] = Tela.objects.filter(pk=pk).first()
        return context

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
            print(request.GET['categoria'])
            if request.GET['extension'] == 'excel':
                return HttpResponseRedirect(reverse_lazy('telas:tela_list'))
            telas = Tela.objects.filter(fecha_eliminacion__isnull=True).order_by('nombre')
            buscar_tela = request.GET['tela']
            categoria = request.GET['categoria']
            print(categoria)
            if (categoria == ''):
                nombre = 'Todos'
            else:
                nombre_categoria = Categoria.objects.get(id=categoria)
                nombre = nombre_categoria.descripcion
            if categoria:
                telas = telas.filter(categoria=categoria)
            if buscar_tela:
                telas = telas.filter(Q(codigo__icontains=buscar_tela) | Q(nombre__icontains=buscar_tela))
            
            template = get_template('telas/listado_pdf.html')
            context = {
                'telas': telas,
                'nombre': nombre
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('telas:tela_list'))

class TelaOfertaView(LoginRequiredMixin, ValidatePermissionRequired,generic.ListView):
    model = TelaOferta
    permission_required = 'telas.view_telaoferta'
    template_name = "telas/tela_oferta_list.html"
    login_url = 'bases:login'

    def queryset(self):
        telas_ofertas = TelaOferta.objects.filter(fecha_eliminacion__isnull=True, estado=True)
        buscar_tela = self.request.POST['tela_oferta']
        categoria = self.request.POST['categoria']
        if categoria:
            telas_ofertas = telas_ofertas.select_related('tela').filter(tela__categoria=categoria)
        #categoria = self.request.POST['categoria']
        #if categoria:
        #    telas = telas.filter(categoria=categoria)
        if buscar_tela:
            telas_ofertas = telas_ofertas.select_related('tela').filter(Q(tela__codigo__icontains=buscar_tela) | Q(tela__nombre__icontains=buscar_tela))
        return telas_ofertas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(fecha_eliminacion__isnull=True)
        context['title'] = 'Listado de telas en Oferta'
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data={}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                telas_oferta = self.queryset()
                for tela_oferta in telas_oferta:
                    data.append(tela_oferta.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class TelaOfertaCreate(LoginRequiredMixin, ValidatePermissionRequired,generic.CreateView):
    model=TelaOferta
    permission_required = 'telas.add_telaoferta'
    form_class=TelaOfertaForm
    context_object_name = 'obj'
    template_name="telas/tela_oferta_form.html"
    success_url=reverse_lazy("telas:tela_oferta_list")
    login_url="bases:login"

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_tela':
                data = []
                telas_oferta = TelaOferta.objects.filter(estado=True).values_list('tela_id')
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']),estado=True).exclude(id__in=telas_oferta)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo
                    data.append(item)
            elif action == 'add':
                request_tela_oferta = json.loads(request.POST['tela_oferta'])
                telas = Tela.objects.get(id=request_tela_oferta['tela_id'])
                with transaction.atomic():
                    tela_oferta = TelaOferta()
                    tela_oferta.tela_id = request_tela_oferta['tela_id']
                    tela_oferta.metraje_oferta = request_tela_oferta['metraje_oferta']
                    tela_oferta.precio_oferta = request_tela_oferta['precio_oferta']
                    telas.metraje -= float(tela_oferta.metraje_oferta)
                    print(telas.metraje)
                    print(tela_oferta.metraje_oferta)
                    tela_oferta.descripcion = 'Oferta'
                    tela_oferta.estado=True
                    tela_oferta.user_created_id = self.request.user.id
                    tela_oferta.save()
                    telas.save()

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = 'Hubo un error,intente más tarde'
        return JsonResponse(data, safe=False)


class TelaOfertaUpdate(LoginRequiredMixin,ValidatePermissionRequired, generic.UpdateView):
    model=TelaOferta
    permission_required = 'telas.change_telaoferta'
    form_class=TelaOfertaForm
    context_object_name = 'obj'
    template_name="telas/tela_oferta_edit_form.html"

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)

    def get_detail(self):
        data = []
        oferta=TelaOferta.objects.get(id=self.get_object().id)
        item=oferta.toJSON()
        item['precio_oferta']=oferta.precio_oferta
        item['metraje_oferta']=oferta.metraje_oferta
        item['id_tela']=oferta.tela_id
        data.append(item)
        return data
    
    def get_context_data(self, **kwargs):
        context = super(TelaOfertaUpdate,self).get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        pk = self.kwargs.get('pk')
        context['oferta']=json.dumps(self.get_detail())
        context ['obj'] = TelaOferta.objects.filter(pk=pk).first()
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_tela':
                data = []
                telas_oferta = TelaOferta.objects.filter(estado=True).values_list('tela_id')
                print
                telas  = Tela.objects.filter(Q(codigo__icontains=request.POST['term']),estado=True).exclude(id__in=telas_oferta)
                for tela in telas:
                    item = tela.toJSON()
                    item['text'] = 'TELA: '+ tela.nombre + ' COD: ' + tela.codigo
                    data.append(item)
            elif action == 'edit':   
                request_tela_oferta = json.loads(request.POST['tela_oferta'])
                print(request_tela_oferta)

                telas = Tela.objects.get(id=request_tela_oferta['tela_id'])

                with transaction.atomic():
                    
                    tela_oferta = TelaOferta.objects.get(id=self.get_object().id)
                    print(tela_oferta)
                    tela_oferta.tela_id = request_tela_oferta['tela_id']
                    if ( float ( request_tela_oferta['metraje_oferta']) < (telas.metraje + tela_oferta.metraje_oferta )):
                        print(request_tela_oferta['metraje_oferta'])
                        print(telas.metraje + tela_oferta.metraje_oferta)
                        print(tela_oferta.metraje_oferta)
                        telas.metraje += tela_oferta.metraje_oferta
                        print(telas.metraje)
                        tela_oferta.metraje_oferta = float(request_tela_oferta['metraje_oferta'])
                        print(tela_oferta.metraje_oferta)
                        telas.metraje -= float(tela_oferta.metraje_oferta)
                    
                    tela_oferta.precio_oferta = request_tela_oferta['precio_oferta']
                    print(telas.metraje)
                    print(tela_oferta.metraje_oferta)
                    tela_oferta.descripcion = 'Oferta'
                    tela_oferta.estado=True
                    tela_oferta.user_updated_id = self.request.user.id
                    tela_oferta.save()
                    telas.save()

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class TelaOfertaInvoicePdfView(generic.View):
    def get(self,request, *args, **kwargs):
        try:
            telas_ofertas = TelaOferta.objects.filter(fecha_eliminacion__isnull=True, estado=True)
            buscar_tela = request.GET['tela_oferta']
            categoria = request.GET['categoria']
            if (categoria == ''):
                nombre = 'Todos'
            else:
                nombre_categoria = Categoria.objects.get(id=categoria)
                nombre = nombre_categoria.descripcion
            if categoria:
                telas_ofertas = telas_ofertas.select_related('tela').filter(tela__categoria=categoria)
            if buscar_tela:
                telas_ofertas = telas_ofertas.select_related('tela').filter(Q(tela__codigo__icontains=buscar_tela) | Q(tela__nombre__icontains=buscar_tela))
            
            template = get_template('telas/listado_oferta_pdf.html')
            context = {
                'telas_ofertas': telas_ofertas,
                'nombre': nombre
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('telas:tela_oferta_list'))


def tela_oferta_delete(request,id):
    try:
        tela_oferta= TelaOferta.objects.get(pk=id)
        tela_oferta.fecha_eliminacion = datetime.now()
        tela_oferta.estado = False
        tela_oferta.save()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except TelaOferta.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)