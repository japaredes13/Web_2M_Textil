from django.urls import path
from .views import VentaView, VentaCreate, VentaListadoPdfView, VentaEdit, VentaCobro

urlpatterns = [
    path('ventas/',VentaView.as_view(), name='ventas_list'),
    path('cobro_deuda/',VentaCobro.as_view(), name='ventas_cobro_list'),
    path('ventas/listado/pdf/<int:pk>/', VentaListadoPdfView.as_view(), name='ventas_listado_pdf'),
    path('ventas/create', VentaCreate.as_view(), name='venta_create'),
    path('ventas/<int:pk>/edit/', VentaEdit.as_view(), name='venta_edit'),

]