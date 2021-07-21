from django.urls import path
from .views import ProveedorView, ProveedorCreate, ProveedorEdit, proveedor_delete

urlpatterns = [
    path('proveedores/',ProveedorView.as_view(), name='proveedor_list'),
    path('proveedores/create', ProveedorCreate.as_view(), name='proveedor_create'),
    path('proveedores/<int:pk>/edit', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedores/<int:id>/delete', proveedor_delete, name='proveedor_delete'),
]