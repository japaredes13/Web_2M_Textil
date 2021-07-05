from django.urls import path
from django.contrib.auth import views as auth_views

from bases.views import Home, LoginFormView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bases/login.html'),
        name='logout'),
]
