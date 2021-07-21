from django.urls import path
from .views import ClienteView, ClienteCreate, ClienteEdit, cliente_delete

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name='cliente_list'),
    path('clientes/create', ClienteCreate.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/edit', ClienteEdit.as_view(), name='cliente_edit'),
    path('clientes/<int:id>/delete', cliente_delete, name='cliente_delete'),
]