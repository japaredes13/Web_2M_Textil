from django.urls import path
from .views import *

urlpatterns = [
    #rutas para Usuario
    path('configuracion/',ConfiguracionUsuarioView.as_view(), name='configuracion_usuario_list'),
    path('configuracion/<int:pk>/edit', ConfiguracionUsuarioEdit.as_view(), name='configuracion_usuario_edit'),

    #rutas para Producto
    path('configuracion_producto/',ConfiguracionProductoView.as_view(), name='configuracion_producto_list'),
    path('configuracion_producto/<int:pk>/edit', ConfiguracionProductoEdit.as_view(), name='configuracion_producto_edit'),

    #rutas para Venta
    path('configuracion_venta/',ConfiguracionVentaView.as_view(), name='configuracion_venta_list'),
    path('configuracion_venta/create',ConfiguracionVentaCreate.as_view(), name='configuracion_venta_create'),
    path('configuracion_venta/<int:pk>/edit', ConfiguracionVentaEdit.as_view(), name='configuracion_venta_edit'),

]