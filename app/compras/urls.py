
from django.urls import path
from .views import *

urlpatterns = [
    path('orden_compra/list/', OrdenCompraListView.as_view(), name='orden_compras_list'),
    path('orden_compra/add/', OrdenCompraCreateView.as_view(), name='orden_compra_create'),
    path('orden_compra/delete/<int:pk>/', OrdenCompraDeleteView.as_view(), name='orden_compra_delete'),
    path('orden_compra/listado/pdf', OrdenCompraPdfView.as_view(), name='orden_compra_listado_pdf'),
    path('orden_compra/<int:pk>/update/', OrdenCompraUpdateView.as_view(), name='orden_compra_update'),

    path('compra/list/', CompraListView.as_view(), name='compras_list'),
    path('compras/<int:pk>/add/', CompraCreateView.as_view(), name='compra_create'),
    path('pago_deuda/',CompraPago.as_view(), name='compras_pago_list'),
    path('compras/listado/pdf/<int:pk>/', CompraListadoDetallePdfView.as_view(), name='compras_listado_detalles_pdf'),
    path('compra/delete/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),
    path('compra/listado/pdf', CompraPdfView.as_view(), name='compra_listado_pdf'),
    path('compra/<int:pk>/update/', CompraUpdateView.as_view(), name='compra_update'),

]