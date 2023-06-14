"""
URL configuration for sghu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from core.views import custom_logout
from administration.views import users_list,eliminar_usuario,CrearUsuarioView
from factura.views import manageFactura, manageFacturaUpdateView, userFactura,userPagando, ListaFact_toPDF
from perfil.views import CompletarPerfil,ModPerfil


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('reservation.urls')),
    path('', include('administration.urls')),
    path('custom_logout', custom_logout, name='logout'),
    path('users', users_list, name='users_list'),
    path('eliminar_usuario/<str:username>/', eliminar_usuario, name='eliminar_usuario'),
    path('manageFactura',manageFactura.as_view(),name='manageFactura'),
    path('manageFactura/update/<int:pk>/', manageFacturaUpdateView.as_view(), name='manageFactura_update'),
    path('userFactura', userFactura.as_view(), name='userFactura'),
    path('userPagando/<int:pk>/', userPagando.as_view(), name='userPagando'),
    path('CompletarPerfil', CompletarPerfil.as_view(), name='CompletarPerfil'),
    path('ModPerfil', ModPerfil.as_view(), name='ModPerfil'),
    path('ListaFact_toPDF', ListaFact_toPDF.as_view(), name='ListaFact_toPDF'),
    path('CrearUsuarioView/', CrearUsuarioView.as_view(), name='CrearUsuarioView'),



]