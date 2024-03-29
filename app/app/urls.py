"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   

urlpatterns = [
    path('',include(('bases.urls','bases'), namespace='bases')),
    path('admin/', admin.site.urls),
    path('ubicaciones/',include(('ubicaciones.urls','ubicaciones'), namespace='ubicaciones')),
    path('clientes/',include(('clientes.urls','clientes'), namespace='clientes')),
    path('telas/',include(('telas.urls','telas'), namespace='telas')),
    path('proveedores/',include(('proveedores.urls','proveedores'), namespace='proveedores')),
    path('compras/',include(('compras.urls','compras'), namespace='compras')),
    path('ventas/',include(('ventas.urls','ventas'), namespace='ventas')),
    path('tipos/',include(('tipos.urls','tipos'), namespace='tipos')),
    path('configuracion/',include(('configuracion.urls','configuracion'), namespace='configuracion')),
    path('cajas/',include(('cajas.urls','cajas'), namespace='cajas')),
    path('dashboard',include(('dashboard.urls','dashboard'), namespace='dashboard')),
    path('inventario/',include(('inventario.urls','inventario'), namespace='inventario')),
    path('users/',include(('user.urls','user'), namespace='user')),
]
