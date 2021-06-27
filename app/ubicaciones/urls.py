from django.urls import path
from .views import DepartamentoView, DepartamentoNew, DepartamentoEdit, departamento_inactivar, departamento_eliminar, \
                    CiudadView, CiudadNew, CiudadEdit, ciudad_inactivar, ciudad_eliminar, ciudades_ajax

urlpatterns = [
    path('departamentos/',DepartamentoView.as_view(), name='departamento_list'),
]