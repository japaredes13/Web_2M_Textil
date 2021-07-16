from django.urls import path
from .views import TelaList, TelaList, TelaCreate, TelaEdit, tela_delete

urlpatterns = [
    path('telas/',TelaList.as_view(), name='tela_list'),
    path('telas/create', TelaCreate.as_view(), name='tela_create'),
    path('telas/<int:pk>/edit', TelaEdit.as_view(), name='tela_edit'),
    path('telas/<int:id>/delete', tela_delete, name='tela_delete'),
]