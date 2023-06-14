from django.forms import ModelForm
from django.utils import timezone
from django.forms import *
from django import forms
import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from administration.models import Room
from factura.models import Factura
from reservation.models import Reservacion
from django.utils.html import format_html
from datetime import date, datetime
from datetime import timedelta
import json


class NameWidget(widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return value

class ReservacionForms(ModelForm):
    idRoom = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control hide-field', 'disabled': 'disabled'}),
        label='Habitación',
        to_field_name='id',
        #initial=0,
    )
    def __init__(self, *args, **kwargs):
        name_initial = kwargs.pop('name_initial', None)
        idRoom_initial=kwargs.pop('idRoom_initial', None)
        ci = kwargs.pop('ci', None)
        itsmod=kwargs.pop('itsmod',None)
        super().__init__(*args, **kwargs)
        
        self.fields['name'].initial = name_initial
        self.fields['name'].required = False
        self.fields['name'].label = format_html('Nombre: <strong>{}</strong>', name_initial)
 
        self.fields['idRoom'].required = False
        self.fields['idRoom'].initial = idRoom_initial
        self.fields['idRoom'].label = format_html('Habitación: <strong>{}</strong>', idRoom_initial)
        if(itsmod):
            del self.fields['name']
            del self.fields['idRoom']
            
            
    #Asignar la EDAD
    
             # Extrae el número de identificación del usuario si está presente en los argumentos
        
        
        # Llama al constructor de la clase padre
   
        
        # Calcula la edad a partir del número de identificación si está presente
        if ci:
             # Calcula la fecha de nacimiento a partir de los primeros seis dígitos del número de identificación
            ano = int(ci[:2])
            if ano <= int(str(datetime.now().year - 18)[2:]):
                ano += 2000
            else:
                ano += 1900
            mes = int(ci[2:4])
            dia = int(ci[4:6])
            fecha_nacimiento = datetime(ano, mes, dia)
            
            # Calcula la edad a partir de la fecha de nacimiento
            hoy = datetime.now()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            
            # Asigna la edad como valor inicial del campo 'edad'
            self.fields['edad'].initial = edad
            
        
    class Meta:
        model = Reservacion
        fields = [ 'name','edad', 'metodoDePago', 'fechaDeInicio', 'fechaDeFin', 'idRoom']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'hide-field'}),
            'edad':forms.NumberInput(attrs={'min': 18, 'max': 80,'readonly': 'readonly',}),
            'fechaDeInicio': forms.DateInput(attrs={ 'min': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'), 'id': 'fechaDeInicio', 'class': 'date no-calendar','readonly': 'readonly',}),
            'fechaDeFin': forms.DateInput(attrs={ 'min': (date.today() + timedelta(days=2)).strftime('%Y-%m-%d'), 'id': 'fechaDeFin', 'class': 'date no-calendar','readonly': 'readonly',}),

        }
    

    
    def clean(self):
        cleaned_data = super().clean()
        
        
            
            # Creamos una nueva factura para esta reserva
            #factura = Factura(idRoom=idRoom, metodoDePago=metodoDePago, fechaDeInicio=fechaDeInicio, fechaDeFin=fechaDeFin)
            
            #factura.save()
        itsmod = cleaned_data.get('itsmod', False)
        id_reservacion = self.instance.id
        itsmod = cleaned_data.get('itsmod', False)

        if not itsmod:
            idRoom = cleaned_data.get('idRoom')
            metodoDePago = cleaned_data.get('metodoDePago')
            fechaDeInicio = cleaned_data.get('fechaDeInicio')
            fechaDeFin = cleaned_data.get('fechaDeFin')

            # Buscamos las facturas existentes para esta reserva
            facturas = Factura.objects.filter(idReservacion=id_reservacion)

            # Eliminamos las facturas existentes
            for factura in facturas:
                factura.delete()
        
        
        
        fecha_de_inicio = cleaned_data.get('fechaDeInicio')
        fecha_de_fin = cleaned_data.get('fechaDeFin')
        if Reservacion.objects.count() >= 20:
            raise forms.ValidationError("No se pueden crear más de 20 reservaciones")

        if fecha_de_inicio and fecha_de_fin:
             print(fecha_de_inicio)
             print(fecha_de_fin)
        # Obtener la fecha actual en la zona horaria de La Habana
        fecha_hora_actual = datetime.now()
        zona_horaria_habana = pytz.timezone('America/Havana')
        fecha_hora_habana = fecha_hora_actual.astimezone(zona_horaria_habana)
        fecha_actual_habana = fecha_hora_habana.date()

        # Calcular la fecha mínima para inicio y fin
        fecha_minima_inicio = fecha_actual_habana + timezone.timedelta(days=1)
        fecha_minima_fin = fecha_actual_habana + timezone.timedelta(days=2)

        # Validar la fecha de inicio
        if fecha_de_inicio < fecha_minima_inicio:
            raise forms.ValidationError("La fecha de inicio debe ser igual o posterior a mañana.")

        # Validar la fecha de fin
        if fecha_de_fin < fecha_minima_fin:
            raise forms.ValidationError("La fecha de fin debe ser igual o posterior a dentro de dos días.")

        # Validar  que la fecha de fin sea posterior a la fecha de inicio
        if fecha_de_inicio > fecha_de_fin:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        if fecha_de_inicio == fecha_de_fin:
            raise forms.ValidationError("No se puede reservar fecha de fin e inicio para el mismo día.")
         #validacion  que el rango de fechas elegidas no exista dentro de las fechas de las de las reservaciones
         
        
        
              
             
        
                    
        return cleaned_data
def calcularEdad():
    
    return edad