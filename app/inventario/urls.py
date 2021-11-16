from django.urls import path
from .views import *

urlpatterns = [
    path('inventario/',InventarioView.as_view(), name='inventario_list'),
    path('inventario/create', InventarioCreate.as_view(), name='inventario_create'),
    path('inventario/listado/pdf/<int:pk>/', InventarioListadoPdfView.as_view(), name='inventario_listado_pdf'),
    path('inventario/listado_completo/pdf/<int:pk>/', InventarioListadoCompletoPdfView.as_view(), name='inventario_listado_completo_pdf'),

]