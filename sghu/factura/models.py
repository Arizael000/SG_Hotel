from django.db import models
from django.contrib.auth.models import User
from administration.models import Room
from reservation.models import Reservacion
# Create your models here.

class Factura(models.Model):
	metodoDePago=models.CharField(max_length=11)
	fechaDeInicio=models.DateField()
	fechaDeFin=models.DateField()
	monto=models.FloatField()
	idUsuario=models.ForeignKey(User,on_delete=models.CASCADE)
	idRoom=models.ForeignKey(Room,on_delete=models.CASCADE)
	idReservacion=models.ForeignKey(Reservacion, on_delete=models.CASCADE)
	pagada=models.BooleanField(default=False)
	


	def __str__(self):
		return self.ID
