from django.urls import path
from .views import ClienteView, ClienteList, ClienteNew, ClienteEdit, cliente_inactivar, cliente_eliminar

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name='cliente_list'),
    path('clientes/ajax_list',ClienteList.as_view(), name='cliente_list_ajax'),
    path('clientes/new', ClienteNew.as_view(), name='cliente_new'),
    path('clientes/edit/<int:pk>', ClienteEdit.as_view(), name='cliente_edit'),
    path('clientes/Inactivar/<int:id>', cliente_inactivar, name='cliente_inactivar'),
    path('clientes/eliminar/<int:id>', cliente_eliminar, name='cliente_delete'),
]