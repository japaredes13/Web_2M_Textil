from django.urls import path
from .views import CategoriaCreate, CategoriaView, CategoriaCreate, CategoriaEdit, categoria_delete, \
                    DisenhoCreate, DisenhoView, DisenhoCreate, DisenhoEdit, disenho_delete

urlpatterns = [
    #rutas para categoria
    path('categorias/',CategoriaView.as_view(), name='categoria_list'),
    path('categorias/create',CategoriaCreate.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/edit', CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/<int:id>/delete',categoria_delete, name='categoria_delete'),

    #rutas para disenho
    path('disenhos/',DisenhoView.as_view(), name='disenho_list'),
    path('disenhos/create',DisenhoCreate.as_view(), name='disenho_create'),
    path('disenhos/<int:pk>/edit', DisenhoEdit.as_view(), name='disenho_edit'),
    path('disenhos/<int:id>/delete',disenho_delete, name='disenho_delete'),
]