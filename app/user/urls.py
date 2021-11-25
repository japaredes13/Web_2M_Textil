from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    # user
    path('users/', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    #path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]
