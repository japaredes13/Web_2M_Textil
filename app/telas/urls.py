from django.urls import path
from .views import TelaInvoicePdfView, TelaList, TelaList, TelaCreate, TelaEdit, tela_delete

urlpatterns = [
    path('telas/',TelaList.as_view(), name='tela_list'),
    path('telas/create', TelaCreate.as_view(), name='tela_create'),
    path('telas/<int:pk>/edit', TelaEdit.as_view(), name='tela_edit'),
    path('telas/listado/pdf', TelaInvoicePdfView.as_view(), name='tela_listado_pdf'),
    path('telas/<int:id>/delete', tela_delete, name='tela_delete'),
]