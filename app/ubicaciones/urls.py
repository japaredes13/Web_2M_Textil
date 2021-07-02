from django.urls import path
from .views import CiudadCreate, DepartamentoView, DepartamentoCreate, DepartamentoEdit, departamento_inactivar, departamento_delete, \
                    CiudadView, CiudadCreate, CiudadEdit, ciudad_inactivar, ciudad_delete, ciudades_ajax

urlpatterns = [
    #rutas para departamento
    path('departamentos/',DepartamentoView.as_view(), name='departamento_list'),
    path('departamentos/create',DepartamentoCreate.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/edit', DepartamentoEdit.as_view(), name='departamento_edit'),
    path('departamentos/<int:id>/delete',departamento_delete, name='departamento_delete'),
    #rutas para ciudad
    path('ciudades/',CiudadView.as_view(), name='ciudad_list'),
    path('ciudades/create',CiudadCreate.as_view(), name='ciudad_create'),
    path('ciudades/<int:pk>/edit',CiudadEdit.as_view(), name='ciudad_edit'),
    path('ciudades/<int:id>/delete',ciudad_delete, name='ciudad_delete'),

]