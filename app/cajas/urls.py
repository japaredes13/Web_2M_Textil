from django.urls import path
from .views import *

urlpatterns = [
    path('cajas/',CajaList.as_view(), name='caja_list'),
    path('cajas/create', CajaCreate.as_view(), name='caja_create'),
    path('cajas/listado/pdf/<int:pk>/', CajaListadoPdfView.as_view(), name='cajas_listado_pdf'),
    path('cajas/<int:pk>/edit', CajaEdit.as_view(), name='caja_edit'),

    path('cajas/bancos',BancoView.as_view(), name='banco_list'),
    path('cajas/bancos/create',BancoCreate.as_view(), name='banco_create'),
    path('cajas/bancos/<int:pk>/edit', BancoEdit.as_view(), name='banco_edit'),
    path('cajas/<int:id>/delete',banco_delete, name='banco_delete'),

    path('movimientos/list', CajaMovimientoList.as_view(), name='movimientos_list'),
    path('movimientos/create', CajaMovimientoCreate.as_view(), name='movimiento_create'),
    path('movimientos/<int:pk>/edit', CajaMovimientoEdit.as_view(), name='movimiento_edit'),
]
