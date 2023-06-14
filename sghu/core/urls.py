from django.contrib.auth import views as auth_views
#from .forms import autenticaForm
from django.urls import path
from . import views
from administration.views import ListaRoom
from core.views import CustomLoginView

app_name='core'


    


urlpatterns=[
    path('', views.principal, name='principal'),
    path('signup',views.signup, name='signup'),
   # path('login',auth_views.LoginView.as_view(template_name='login.html',authentication_form=autenticaForm),name='login'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('modificarPerfil',views.modPerfil,name='modificarPerfil'),
    path('articleOne', views.articleOne, name='articleOne'),
    path('articleTwo', views.articleTwo, name='articleTwo'),
    path('articleThree', views.articleThree, name='articleThree'),
    path('articleFour', views.articleFour, name='articleFour'),
    
    path('perfil',views.perfil, name='perfil'),
    path('eliminar_usuario', views.eliminar_usuario, name='eliminar_usuario'),
    path('habitaciones', views.Habitaciones, name='habitaciones'),
    path('troll', views.troll,name='troll')
    
 ]
