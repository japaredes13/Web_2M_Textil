from django.urls import path
from .views import VentaView, VentaCreate

urlpatterns = [
    path('ventas/',VentaView.as_view(), name='ventas_list'),
    path('ventas/create', VentaCreate.as_view(), name='venta_create'),
]