from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from bases.mixins import ValidatePermissionRequired
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.hashers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from user.forms import UserForm, RolForm
from user.models import User
from django.db.models import Q
import json
from django.db.models import ProtectedError


class UserListView(LoginRequiredMixin,ValidatePermissionRequired, ListView):
    model = User
    template_name = 'users/user_list.html'
    #permission_required = 'user.change_user'

    def queryset(self):
        usuario = self.request.POST['usuario']
        usuarios = User.objects.filter(Q(first_name__icontains=usuario) | Q(last_name__icontains=usuario) | Q(username__icontains=usuario))
        return usuarios

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                usuarios = self.queryset()
                for i in usuarios:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        return context


class UserCreateView(LoginRequiredMixin,ValidatePermissionRequired, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user:user_list')
    #permission_required = 'user.view_user'
    url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            user_request =  json.loads(request.POST['user'])
            if action == 'add':
                with transaction.atomic():
                    user_request =  json.loads(request.POST['user'])
                    user = User()

                    user.first_name = user_request['first_name']
                    user.last_name = user_request['last_name']
                    user.email = user_request['email']
                    user.username = user_request['username']
                    password = user_request['password1']
                    user.password = make_password(password)
                    user.save()
                    user.user_permissions.set(user_request['permisos'])
                    user.groups.set(user_request['groups'])

                    user.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print('ERROOOOR:   ' +str(e))
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Datos del Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user:user_list')
    #permission_required = 'user.change_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            user_request =  json.loads(request.POST['user'])
            if action == 'edit':
                with transaction.atomic():
                    user_request =  json.loads(request.POST['user'])
                    user = self.get_object()

                    user.first_name = user_request['first_name']
                    user.last_name = user_request['last_name']
                    user.email = user_request['email']
                    user.username = user_request['username']
                    password = user_request['password1']
                    user.password = make_password(password)
                    user.save()
                    user.user_permissions.set(user_request['permisos'])
                    user.groups.set(user_request['groups'])

                    user.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


def user_delete(request,id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except User.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    except ProtectedError:
        data = {
            'error':True,
            'message':'No se ha eliminado. El registro se encuentra asociado con otras informaciones. Comuníquese con soporte!.'
        }
    return JsonResponse(data, safe=False)


class RolListView(ListView):
    model = Group
    template_name ='users/rol_list.html'
    #permission_required ='auth.view_user'
	
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context ['obj'] = self.get_queryset()
        return context


class RolCreateView(CreateView):
	#error_css_class = 'error'
    model = Group
    template_name = 'users/rol_form.html'
    form_class = RolForm
    context_object_name = 'form'
    success_url = reverse_lazy('user:rol_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RolEditView(UpdateView):
	#error_css_class = 'error'
	model = Group
	template_name = 'users/rol_form.html'
	form_class = RolForm
	context_object_name = 'obj'
	success_url = reverse_lazy('user:rol_list')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

def rol_delete(request,id):
    try:
        grupo= Group.objects.get(pk=id)
        grupo.delete()
        data = {
            'error':False, 
            'message':"Registro eliminado correctamente."
        }
    except Group.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)