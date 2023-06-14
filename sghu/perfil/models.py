from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.


class Perfil(models.Model):
    ci = models.CharField(max_length=11, validators=[RegexValidator(regex='^[0-9]{11}$', message='El CI debe tener 11 dígitos')],blank=False)
    phone = models.CharField(max_length=8, validators=[RegexValidator(regex='^5[0-9]{7}$', message='El número de teléfono debe comenzar con 5 y tener 8 dígitos')],blank=False)
    adress=models.CharField(max_length=30)
    bio=models.TextField(max_length=500)
    usuarioRelacionado=models.OneToOneField(User,on_delete=models.CASCADE)