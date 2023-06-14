from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder':'Nombre de usuario', 
        'class': 'form-control py-2 px-6 rounded-lg' 
        }))
    email=forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control py-2 px-6 rounded-lg'
        }))
    password1=forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Tu contraseña',
        'class': 'form-control py-2 px-6 rounded-lg'
        }))
    password2=forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirma tu contraseña',
        'class': 'form-control py-2 px-6 rounded-lg'
        }))
    
    
class autenticaForm(AuthenticationForm):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder':'Nombre de usuario', 
        'class': 'form-control py-2 px-6 rounded-lg' 
        }))
    password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Tu contraseña',
        'class': 'form-control py-2 px-6 rounded-lg'
        }))