from django.forms import ModelForm
from django.forms import *
from django import forms
import pytz
from django.utils.html import format_html
from datetime import date, timedelta
from .models import Perfil
from datetime import datetime


class NameWidget(widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return value

class PerfilForms(forms.ModelForm):
    ci = forms.CharField(label='Carnet de identidad (Necesario):')
    phone = forms.IntegerField(label='Teléfono (Necesario):')
    adress = forms.CharField(label='Dirección:')
    bio = forms.CharField(label='Biografía:', widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['adress'].required = False
        self.fields['bio'].required = False
    
    
    
    
    class Meta:
        model = Perfil
        fields = ['ci', 'phone', 'adress', 'bio']
        widgets = {
            'ci': forms.TextInput(attrs={'class': 'hide-field','class': 'form-control py-2 px-6 rounded-lg',
             'placeholder':'Ejemplo: 12121289121' ,'type': 'number','id':'id_ci'                      }),
            
            'phone': forms.TextInput(attrs={'class': 'form-control py-2 px-6 rounded-lg',
                                 'placeholder': 'Ejemplo: 51111111', 'type': 'number', 'id': 'id_ph',
                                  'pattern': '[0-9]{8}', 'maxlength': '8'}),
            
            'adress': forms.TextInput(attrs={'maxlength': 30,'class': 'form-control py-2 px-6 rounded-lg',
              'placeholder':'Ejemplo: Calle 30 E/ ave 20 y 25 #8509 Boyeros La Habana'                                }),
            
            'bio': forms.Textarea(attrs={'maxlength': 500,'class': 'form-control py-2 px-6 rounded-lg',
             'placeholder':'Un poco de información sobre usted'                            }),
        }
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not (50000000 <= int(phone) <= 59999999):
            raise forms.ValidationError('El número de teléfono debe comenzar con 5 y tener 8 dígitos')
        return phone
        
    def clean_ci(self):
        ci = self.cleaned_data['ci']
        if not (len(ci) == 11 and ci.isdigit()):
            raise forms.ValidationError('El CI debe tener 11 dígitos')
        
         # Obtener el año actual menos 18
        ano_maximo = datetime.now().year - 18
    
     # Obtener el año de nacimiento a partir de los dos primeros dígitos del número de identificación
        ano = int(ci[:2])
        if ano <= int(str(ano_maximo)[2:]):
         ano += 2000
        else:
          ano += 1900

    # Verificar que el año de nacimiento está entre 1944 y el año actual menos 18
        if ano < 1944 or ano > ano_maximo:
            raise forms.ValidationError('No cumple con la edad necesaria')
    
    # Obtener el mes y el día de nacimiento a partir de los siguientes cuatro dígitos del número de identificación
        mes = int(ci[2:4])
        dia = int(ci[4:6])
    
    # Verificar que el mes y el día de nacimiento son válidos
        try:
          datetime(ano, mes, dia)
        except ValueError:
          raise forms.ValidationError('El mes y/o día de nacimiento no son válidos')
    
        
        return ci
        
