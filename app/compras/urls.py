
from django.urls import path
from .views import CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView

urlpatterns = [
    path('compra/list/', CompraListView.as_view(), name='compras_list'),
    path('compra/add/', CompraCreateView.as_view(), name='compra_create'),
    path('compra/delete/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),
    path('compra/update/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),

]