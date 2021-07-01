from django.urls import path
from .views import CiudadCreate, DepartamentoView, DepartamentoCreate, DepartamentoEdit, departamento_inactivar, departamento_eliminar, \
                    CiudadView, CiudadCreate, CiudadEdit, ciudad_inactivar, ciudad_eliminar, ciudades_ajax

urlpatterns = [
    path('departamentos/',DepartamentoView.as_view(), name='departamento_list'),
    path('departamentos/create',DepartamentoCreate.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/edit', DepartamentoEdit.as_view(), name='departamento_edit'),

    path('ciudades/',CiudadView.as_view(), name='ciudad_list'),
    path('ciudades/create',CiudadCreate.as_view(), name='ciudad_create'),
    path('ciudades/<int:pk>/edit',CiudadEdit.as_view(), name='ciudad_edit'),


]