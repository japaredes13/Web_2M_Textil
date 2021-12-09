from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


#Funcion que valida  los permisos que tiene el usuario logueado
class ValidatePermissionRequired(object):
    permission_required = ''
    url_redirect = None
    

    def get_perms(self):
        if isinstance(self.permission_required,str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    
    def get_url(self):
        if self.url_redirect is None:
           return reverse_lazy('bases:home')
        return self.url_redirect    

    def dispatch(self,request,*args,**kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request,*args,**kwargs)
        messages.error(request,'No tiene permiso para ingresar a este módulo')
        return redirect(self.get_url())
        