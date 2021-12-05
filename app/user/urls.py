from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    # user
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:id>/delete/',user_delete, name='user_delete'),
    
    # rol
    path('users/roles/', RolListView.as_view(), name='rol_list'),
    path('users/roles/create', RolCreateView.as_view(), name='rol_create'),
    path('users/roles/<int:pk>/edit', RolEditView.as_view(), name='rol_edit'),
    path('users/roles/<int:id>/delete', rol_delete, name='rol_delete'),
]
