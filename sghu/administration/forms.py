from django.forms import ModelForm
from django.forms import *
from django import forms
from .models import Room
from django.utils.html import format_html



class RoomForm(ModelForm):
   
    def __init__(self, *args, **kwargs):
       # name_initial = kwargs.pop('name_initial', None)
        super().__init__(*args, **kwargs)
        self.fields['idHotel'].initial = 1
        
    class Meta:
        model = Room
        fields = ['description','price','ventilacion','temperaturaAgua','television','idHotel']
        
        widgets = {
            'description': forms.TextInput(attrs={}),
            
        }
        
