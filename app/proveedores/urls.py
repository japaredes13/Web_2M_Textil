from django.urls import path
from .views import ProveedorView,ProveedorList, ProveedorNew, ProveedorEdit, proveedor_inactivar, proveedor_eliminar

urlpatterns = [
    path('proveedores/',ProveedorView.as_view(), name='proveedor_list'),
    path('proveedores/ajax_list',ProveedorList.as_view(), name='proveedor_list_ajax'),
    path('proveedores/new', ProveedorNew.as_view(), name='proveedor_new'),
    path('proveedores/edit/<int:pk>', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedores/Inactivar/<int:id>', proveedor_inactivar, name='proveedor_inactivar'),
    path('proveedores/eliminar/<int:id>', proveedor_eliminar, name='proveedor_delete'),
]