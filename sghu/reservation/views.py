from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render, redirect
from .forms import ReservacionForms
from .models import Reservacion
from django.views.generic import DeleteView, ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from administration.models import Room
from factura.models import Factura
from datetime import timedelta
from datetime import date, datetime
import json
from django import forms
from perfil.models import Perfil
# Create your views here.

      
        
                
                
class CrearReservacion(LoginRequiredMixin,CreateView):
    
    model = Reservacion
    template_name = 'realizarReservacion.html'
    form_class = ReservacionForms
    
    success_url = reverse_lazy('listarReservaciones')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = self.request.user.perfil
            if not perfil.ci or not perfil.phone:
                return redirect('CompletarPerfil')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
         return redirect('core:login')
    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.username
        initial['idRoom']=get_object_or_404(Room, pk=self.kwargs['pk'])
        return initial
    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs['name_initial']=self.request.user.username
        kwargs['idRoom_initial']=get_object_or_404(Room, pk=self.kwargs['pk'])
        kwargs['ci']=Perfil.objects.get(usuarioRelacionado=self.request.user).ci
        return kwargs
    
    def form_valid(self, form):
        form.instance.name = self.request.user.username
        form.instance.idUsuario = self.request.user
        form.instance.idRoom=get_object_or_404(Room, pk=self.kwargs['pk'])
        
        #Validacion de superposicion de fechas
        #Fechas Elegidas
        fechasElegidas = []
        fechaInicioIterar = form.cleaned_data['fechaDeInicio']
        
        while fechaInicioIterar <=form.cleaned_data['fechaDeFin']:
                fechasElegidas.append(fechaInicioIterar)
                fechaInicioIterar += timedelta(days=1)
        print("Fechas Elegidas")
        print(fechasElegidas)
        
        #Fechas Reservadas
        fechasReservadas=[]
        reservaciones = Reservacion.objects.filter(idRoom=get_object_or_404(Room, pk=self.kwargs['pk']))
        print(reservaciones)
        if reservaciones.exists():
            for reservacion in reservaciones:
                fechitaIni=reservacion.fechaDeInicio
                fechitaFin=reservacion.fechaDeFin
                while fechitaIni <= fechitaFin:
                  fechasReservadas.append(fechitaIni)
                  fechitaIni += timedelta(days=1)
        print("Fechas Reservadas")
        print(fechasReservadas)
        
        for E in fechasElegidas:
            if E in fechasReservadas:
                print("Que loco voldemort")
                form.add_error(None, 'La reserva se superpone con otra reserva existente, elija un rango de fechas correcto')
                return self.form_invalid(form)
        
        return super().form_valid(form)
    def form_invalid(self, form):
        
        form.fields['name'].initial = self.request.user.username
        form.fields['idRoom'].initial = get_object_or_404(Room, pk=self.kwargs['pk'])
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         
        fechas_no_disponibles_inicio = []#esta es la lista de las fechas que voy a deshabilitar
        for reservacion in Reservacion.objects.filter(idRoom=get_object_or_404(Room, pk=self.kwargs['pk'])):
            startDate = reservacion.fechaDeInicio
            endDate = reservacion.fechaDeFin

            fechaActual = startDate   #esta es la fecha para trabajar en el while

            while fechaActual <= endDate:
                if datetime.combine(fechaActual, datetime.min.time()) < datetime.min or datetime.combine(fechaActual, datetime.min.time()) > datetime.max:
                     break
                fechas_no_disponibles_inicio.append(fechaActual)  
                fechaActual += timedelta(days=1)
            
            
        lista = [f.strftime('%Y-%m-%d') for f in fechas_no_disponibles_inicio]
        context['fechas_no_disponibles_inicio']=lista
        return context
    
    
    #esto es pa coger las fechas
def daterange(start_date, end_date):
      for n in range(int((end_date - start_date).days)):
         yield start_date + timedelta(n)    

class ModificarReservacion(LoginRequiredMixin,UpdateView):
    model = Reservacion
    template_name = 'modificarReservacion.html'
    form_class = ReservacionForms
    success_url = reverse_lazy('listarReservaciones')
    def dispatch(self, request, *args, **kwargs):
      if request.user.is_authenticated:
            perfil = self.request.user.perfil
            if not perfil.ci or not perfil.phone:
                return redirect('CompletarPerfil')
            else:
                return super().dispatch(request, *args, **kwargs)
      else:
         return redirect('core:login')
     
     
    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.username
        return initial
    def get_object(self):
        return Reservacion.objects.get(pk=self.kwargs['pk'])
    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs['name_initial']=self.request.user.username
        kwargs['itsmod']=True
        return kwargs
    def form_valid(self, form):
        form.instance.name = self.request.user.username
        form.instance.idUsuario = self.request.user
        return super().form_valid(form)
    def form_invalid(self, form):
        # Volver a establecer el valor inicial de 'name' en caso de errores de validación en otros campos del formulario.
        form.fields['name'].initial = self.request.user.username
        return self.render_to_response(self.get_context_data(form=form))
from core.views import updateDisponibilidad
class ListaReservacion(LoginRequiredMixin,ListView):
    updateDisponibilidad()
    model = Reservacion
    template_name = 'gestionarReservacion.html'
    queryset = Reservacion.objects.all()#.order_by('created_at')
    #Pa lo del usuario anonimo y los que no han completado el perfil
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = self.request.user.perfil
            if not perfil.ci or not perfil.phone:
                return redirect('CompletarPerfil')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
         return redirect('core:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservasPropias=Reservacion.objects.filter(idUsuario=self.request.user.id)
        #Facturas
        facturas=Factura.objects.filter(idUsuario=self.request.user.id)
        context['facturas']=facturas
        #Pasar las habitaciones al contexto de la tempalte
        rooms = Room.objects.all()
        image_names = ['1.jpg', '2.jpg', '3.jpg','4.jpg']
        context['rooms'] = rooms
        context['image_names'] = image_names
        context['reservasPropias']=reservasPropias
        return context


class EliminarReservacion(LoginRequiredMixin,DeleteView):
    model = Reservacion
    template_name = 'eliminarReservacion.html'
    def get_success_url(self):
         #referer = self.request.META.get('HTTP_REFERER')
         #if referer and 'manageReservation' in referer:
           # return reverse_lazy('manageReservation')
         #else:
            return reverse_lazy('listarReservaciones')

class EliminarReservacionbyAdmin(LoginRequiredMixin,DeleteView):
    model = Reservacion
    template_name = 'eliminarReservacionbyAdmin.html'
    def get_success_url(self):
         #referer = self.request.META.get('HTTP_REFERER')
         #if referer and 'manageReservation' in referer:
           # return reverse_lazy('manageReservation')
         #else:
            return reverse_lazy('manageReservation')

