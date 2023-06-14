from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.models import User
from administration.models import Room
from reservation.models import Reservacion
from factura.models import Factura
from perfil.models import Perfil
from django.contrib.auth.decorators import user_passes_test
from .forms import autenticaForm
# Create your views here.

def user_is_not_authenticated(user):
    return not user.is_authenticated


def principal(request):
    updateDisponibilidad()
    #usuario_pertenece_a_grupo = request.user.groups.filter(name='Clientes').exists()
    #context = {'usuario_pertenece_a_grupo': usuario_pertenece_a_grupo}
    return render(request, 'principal.html')
def articleOne(request):
    return render(request,'1article.html')

def articleTwo(request):
    return render(request,'2article.html')

def articleThree(request):
    return render(request,'3article.html')

def articleFour(request):
    return render(request,'4article.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = autenticaForm

    def form_valid(self, form):
        # Llamamos a la implementación de form_valid de LoginView
        response = super().form_valid(form)

        # Verificamos si el usuario tiene los campos ci y phone en su perfil
        perfil = self.request.user.perfil
        if not perfil.ci or not perfil.phone:
            # Si los campos están nulos, redirigimos al usuario a completar su perfil
            return redirect('CompletarPerfil')
        
        # Si los campos no están nulos, redirigimos al usuario a su dashboard
        return redirect('core:principal')
    
    
    
    
    
    
@user_passes_test(user_is_not_authenticated)
def signup(request):
    data={'form':SignupForm()}

    if request.method == 'POST':
        form= SignupForm(data=request.POST)

        if form.is_valid():
            
            form.save()
            perfil = Perfil.objects.create(
                usuarioRelacionado=User.objects.get(username=request.POST['username'])
            )
                        
            

            username2 = request.POST['username']
            password2 = request.POST['password1']
            user = authenticate(request, username=username2, password=password2)
            
            if user is not None:
                login(request, user)
                return redirect('CompletarPerfil')
            else:
                # Handle invalid login credentials
             pass
       
    else:
    
        form=SignupForm()

    return render(request, 'signup.html',{
        'form':form
    })

def custom_logout(request):
        logout(request)
        return redirect('../')
    
@login_required
def perfil(request):
    context = {}
    try:
        context['perfil'] = Perfil.objects.get(usuarioRelacionado=request.user)
    except Perfil.DoesNotExist:
        pass
    return render(request, 'perfil.html', context)
@login_required
def modPerfil(request):
    usuario = request.user
    if request.method == 'POST':
        usuario.username = request.POST['usermod']
        usuario.email = request.POST['emailmod']
        usuario.first_name = request.POST['nombremod']
        usuario.last_name=request.POST['apellmod']
        usuario.save()
        return redirect('core:perfil')
    else:

      return render(request, 'modificarPerfil.html', {'usuario': usuario})



@login_required
def eliminar_usuario(request):
    if request.method=='POST':
         nombreU=request.user.username
         
         logout(request)
         objeto = get_object_or_404(User, username=nombreU)
         objeto.delete()
         return redirect('core:principal')
        
    else:
        return render(request, 'eliminar_usuario.html')
@login_required
def Habitaciones(request):
    updateDisponibilidad()
    
    rooms = Room.objects.all()
    image_names = ['1.jpg', '2.jpg', '3.jpg','4.jpg']
    context = {'rooms': rooms,'image_names':image_names}
    if request.user.is_authenticated:
     perfil = request.user.perfil
     if not perfil.ci or not perfil.phone:
            # Si los campos están nulos, redirigimos al usuario a completar su perfil
            return redirect('CompletarPerfil')
    return render(request, 'habitaciones.html', context)


def updateDisponibilidad():
     
     rooms=Room.objects.all()
     reservas=Reservacion.objects.all()
     facturas=Factura.objects.all()
     
     
     
     for e in reservas:
         fechafinmajuno =e.fechaDeFin + datetime.timedelta(days=1)
         fechaIniciomenojdo=e.fechaDeInicio - datetime.timedelta(days=2)
         if(fechaIniciomenojdo <= datetime.date.today()):
             for f in facturas:
                 
               if f.idReservacion == e:    
                 e.delete()
             return None
         if(fechafinmajuno <= datetime.date.today()):
             habitacion=rooms.get(id=e.idRoom.id)
             habitacion.disponible=True
             habitacion.save()
             e.delete()
             return None
         if(e.fechaDeInicio>=datetime.date.today() and e.fechaDeFin>datetime.date.today()):
             habitacion=rooms.get(id=e.idRoom.id)
             habitacion.disponible=False
             habitacion.save()
     
     return None
def troll(request):
    return render(request,'403_troll.html')



