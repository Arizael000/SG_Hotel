from django.contrib.auth.models import User
from core.models import Hotel
from .models import Room
from reservation.models import Reservacion
from administration.forms import RoomForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, ListView, CreateView, UpdateView, View
from .UserForm import UserForm, CrearUsuarioForm
from django.contrib.auth.forms import UserCreationForm
from perfil.models import Perfil
from django.contrib.auth.models import Group

class CrearUsuarioView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self, request):
        form = CrearUsuarioForm()
        context = {'form': form}
        return render(request, 'crear_usuario.html', context)
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_staff']
            user.save()
            perfil = Perfil.objects.create(
                usuarioRelacionado=User.objects.get(username=request.POST['username'])
            )
            return redirect('users_list')
        context = {'form': form}
        return render(request, 'crear_usuario.html', context)



@login_required
def users_list(request):
    # Obtener la lista de usuarios del sistema
    users = User.objects.all()

    # Pasar la lista de usuarios al template
    context = {'users': users}
    return render(request, 'users_list.html', context)

@login_required
def manageReservations(request):
        reservations=Reservacion.objects.all()
        rooms=Room.objects.all()
        context={'reservations':reservations,'rooms':rooms}
        perfil = request.user.perfil
        if not perfil.ci or not perfil.phone:
            # Si los campos están nulos, redirigimos al usuario a completar su perfil
            return redirect('CompletarPerfil')
        return render(request, 'manageReservation.html', context)

@login_required
def eliminar_usuario(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('users_list')

#Vistas basadas en clase de las habitaciones
class CrearRoom(LoginRequiredMixin,CreateView):
    model = Room
    template_name = 'anadirRoom.html'
    form_class = RoomForm
    queryset = Room.objects.all()
    success_url = reverse_lazy('listarRoom')
    
    def dispatch(self, request, *args, **kwargs):
        perfil = self.request.user.perfil
        if not perfil.ci or not perfil.phone:
            return redirect('CompletarPerfil')
        return super().dispatch(request, *args, **kwargs)
    def get_initial(self):
        initial = super().get_initial()
        initial['idHotel'] = 1
        return initial
    def form_valid(self, form):
        # Comprobamos si existe alguna habitación con la descripción proporcionada
        if Room.objects.filter(description=form.cleaned_data['description']).exists():
            form.add_error('description', 'Ya existe una habitación con esta descripción.')
            return super().form_invalid(form)
    
        
        return super().form_valid(form)
    def get_queryset(self):
        return Room.objects.all() 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # NOOOOO Condicionales para habitaciones para crear
    #     if self.queryset.count() >= 20:
    #         context['todasHabitaciones'] = True
    #     else:
    #    #     context['todasHabitaciones'] = False
      #  context['habitaciones']=20-self.queryset.count()
        
        return context


class ListaRoom(LoginRequiredMixin,ListView):
    model = Room
    template_name = 'manageroom.html'
    queryset = Room.objects.all().order_by('-price')
    
    def dispatch(self, request, *args, **kwargs):
        perfil = self.request.user.perfil
        if not perfil.ci or not perfil.phone:
            return redirect('CompletarPerfil')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Condicionales para habitaciones para crear
        if self.queryset.count() >= 20:
            context['todasHabitaciones'] = True
        else:
            context['todasHabitaciones'] = False
        disponibles=20-self.queryset.count()
        context['habitaciones']=20-self.queryset.count()
        
        return context

class EliminarRoom(LoginRequiredMixin,DeleteView):
    model = Room
    template_name = 'eliminarRoom.html'
    success_url = reverse_lazy('listarRoom')
    
    def dispatch(self, request, *args, **kwargs):
        perfil = self.request.user.perfil
        if not perfil.ci or not perfil.phone:
            return redirect('CompletarPerfil')
        return super().dispatch(request, *args, **kwargs)
    

class ModRoom(LoginRequiredMixin,UpdateView):
    model = Room
    template_name = 'modRoom.html'
    form_class = RoomForm
    success_url = reverse_lazy('listarRoom')
    
    def dispatch(self, request, *args, **kwargs):
        perfil = self.request.user.perfil
        if not perfil.ci or not perfil.phone:
            return redirect('CompletarPerfil')
        return super().dispatch(request, *args, **kwargs)
    
class editarUsuario(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(instance=user)
        context = {'form': form, 'user': user}
        return render(request, 'editUser.html', context)

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_active = request.POST.get('is_active') == 'on'
            user.is_staff = request.POST.get('is_staff') == 'on'
            user.is_superuser = request.POST.get('is_superuser') == 'on'
            user_permissions = form.cleaned_data['user_permissions']
            user.user_permissions.set(user_permissions)
        if not user.is_staff and not user.is_superuser:
            grupo_clientes = Group.objects.get(name='Clientes')
            if grupo_clientes not in user.groups.all():
                user.groups.add(grupo_clientes)
        else:
            grupo_clientes = Group.objects.get(name='Clientes')
            if grupo_clientes in user.groups.all():
                user.groups.remove(grupo_clientes)
        user.save()
        print(request.POST) 
        user.save() 
        return redirect('users_list')