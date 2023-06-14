from django.db import models
from core.models import Hotel
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
#hotel = Hotel.objects.get(id=1, nombre='Hotel UCI')

class Room(models.Model):
    description = models.CharField(max_length=500)
    price = models.IntegerField(null=False, default=500, validators=[MinValueValidator(500), MaxValueValidator(1300)])
    idHotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    ventilacion = models.CharField(
        verbose_name='Ventilacion',
        max_length=15,
        choices=(
            ('acondicionada', 'Acondicionada'),
            ('ventilador', 'Ventilador')
        ),
        default='1'
    )
    temperaturaAgua = models.CharField(
        verbose_name='TemperaturaAgua',
        max_length=10,
        choices=(
            ('fria', 'Fría'),
            ('caliente', 'Caliente')
        ),
        default='1'
    )
    television=models.BooleanField(default=False)
    disponible=models.BooleanField(default=True)
    def __str__(self):
        return self.description