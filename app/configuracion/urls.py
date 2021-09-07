from django.urls import path
from .views import *

urlpatterns = [
    #rutas para departamento
    path('configuracion/',ConfiguracionUsuarioView.as_view(), name='configuracion_usuario_list'),
    path('configuracion/<int:pk>/edit', ConfiguracionUsuarioEdit.as_view(), name='configuracion_usuario_edit'),

]