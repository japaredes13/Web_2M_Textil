from django.urls import path
from .views import *

urlpatterns = [
    path('cajas/',CajaList.as_view(), name='caja_list'),
    path('cajas/create', CajaCreate.as_view(), name='caja_create'),
]