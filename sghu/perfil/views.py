from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PerfilForms
from .models import Perfil

# Create your views here.



    
   
    
class CompletarPerfil(LoginRequiredMixin,UpdateView):
    model = Perfil
    template_name = 'completarPerfil.html'
    form_class = PerfilForms
    success_url = reverse_lazy('listarReservaciones')

    def get_object(self, queryset=None):
        # Obtener el objeto Perfil asociado al usuario actual
        return self.request.user.perfil

    def form_valid(self, form):
        # Asociar el objeto Perfil actual con el usuario actual
        perfil = form.save(commit=False)
        perfil.save()
        return super().form_valid(form)
    
class ModPerfil(LoginRequiredMixin,UpdateView):
    model = Perfil
    template_name = 'modP.html'
    form_class = PerfilForms
    success_url = reverse_lazy('core:perfil')

    def get_object(self, queryset=None):
        # Obtener el objeto Perfil asociado al usuario actual
        return self.request.user.perfil

    def form_valid(self, form):
        # Asociar el objeto Perfil actual con el usuario actual
        perfil = form.save(commit=False)
        perfil.save()
        return super().form_valid(form)
    

class ListaPerfil(LoginRequiredMixin,ListView):
    model = Perfil
    template_name = 'gestionarReservacion.html'
    queryset = Perfil.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context



