from django.urls import path
from .views import TelaInvoicePdfView, TelaList, TelaList, TelaCreate, TelaEdit, tela_delete,TelaOfertaView,TelaOfertaCreate, TelaOfertaInvoicePdfView,TelaOfertaUpdate, tela_oferta_delete

urlpatterns = [
    path('telas/',TelaList.as_view(), name='tela_list'),
    path('telas/create', TelaCreate.as_view(), name='tela_create'),
    path('telas/<int:pk>/edit', TelaEdit.as_view(), name='tela_edit'),
    path('telas/listado/pdf', TelaInvoicePdfView.as_view(), name='tela_listado_pdf'),
    path('telas/<int:id>/delete', tela_delete, name='tela_delete'),

    path('telas/oferta/',TelaOfertaView.as_view(), name='tela_oferta_list'),
    path('telas/oferta/create', TelaOfertaCreate.as_view(), name='tela_oferta_create'),
    path('telas/oferta/<int:pk>/edit/', TelaOfertaUpdate.as_view(), name='tela_oferta_edit'),
    path('telas/oferta/listado/pdf', TelaOfertaInvoicePdfView.as_view(), name='tela_oferta_listado_pdf'),
    path('telas/oferta/<int:id>/delete', tela_oferta_delete, name='tela_oferta_delete'),
    #path('telas/oferta/<int:pk>/edit', TelaOfertaEdit.as_view(), name='tela_oferta_edit'),
]