from django.shortcuts import render, redirect
from django.db import transaction
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from proveedores.models import Proveedor
from .forms import CompraForm
from telas.models import Tela
from .models import Compra, DetCompra


class CompraListView(LoginRequiredMixin, generic.ListView):
    model = Compra
    template_name = 'compras/compras_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Compra.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_telas':
                data = []
                for i in DetCompra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('compras:compra_create')
        context['list_url'] = reverse_lazy('compras:compra_list')
        context['entity'] = 'Compras'
        return context


class CompraCreateView(LoginRequiredMixin, generic.CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compras_form.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_telas':
                data = []
                telas = Tela.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in telas:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    compras = json.loads(request.POST['compras'])
                    compra = Compra()
                    compra.date_joined = compras['date_joined']
                    compra.prov_id = compras['prov']
                    compra.subtotal = float(compras['subtotal'])
                    compra.iva = float(compras['iva'])
                    compra.total = float(compras['total'])
                    compra.user_created_id = self.request.user.id
                    compra.save()
                    for i in compras['telas']:
                        det = DetCompra()
                        det.compra_id = compra.id
                        det.tela_id = i['id']
                        det.metraje = int(i['metraje'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.user_created_id = self.request.user.id
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class CompraUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compras_form.html'
    success_url = reverse_lazy('compras:compras_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_telas':
                data = []
                telas = Tela.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in telas:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    compras = json.loads(request.POST['compras'])
                    #compra = Compra.objects.get(pk=self.get_object().id)
                    compra = self.get_object()
                    compra.date_joined = compras['date_joined']
                    compra.prov_id = compras['prov']
                    compra.subtotal = float(compras['subtotal'])
                    compra.iva = float(compras['iva'])
                    compra.total = float(compras['total'])
                    compra.save()
                    compra.detcompra_set.all().delete()
                    for i in compras['telas']:
                        det = DetCompra()
                        det.compra_id = compra.id
                        det.telas_id = i['id']
                        det.metraje = int(i['metraje'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_telas(self):
        data = []
        try:
            for i in DetCompra.objects.filter(compra_id=self.get_object().id):
                item = i.telas.toJSON()
                item['metraje'] = i.metraje
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_telas())
        return context


class CompraDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Compra
    template_name = 'compras/delete.html'
    success_url = reverse_lazy('compras:compras_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        return context