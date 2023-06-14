from django.db import models
from django.contrib.auth.models import User
from administration.models import Room
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Reservacion(models.Model):
    name = models.CharField(max_length=255)
    edad = models.IntegerField(null=False,validators=[MinValueValidator(18), MaxValueValidator(80)])
    metodoDePago = models.CharField(verbose_name='Metodo de Pago', max_length=10, choices=(
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta')
    ), default='1')
    fechaDeInicio = models.DateField(verbose_name='Fecha de Inicio')
    fechaDeFin = models.DateField(verbose_name='Fecha de Fin')
    idUsuario = models.ForeignKey(User,on_delete=models.CASCADE )
    idRoom=models.ForeignKey(Room,on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        from factura.models import Factura
        super(Reservacion, self).save(*args, **kwargs)
        factura=Factura()
        factura.fechaDeInicio=self.fechaDeInicio
        factura.fechaDeFin=self.fechaDeFin
        factura.metodoDePago=self.metodoDePago
        factura.monto=self.idRoom.price + (((self.fechaDeFin - self.fechaDeInicio).days-1) * self.idRoom.price)+200
        factura.idRoom=self.idRoom
        factura.idUsuario=self.idUsuario
        factura.idReservacion=self
        factura.save()
        
       ####################
       
       
    def delete(self, *args, **kwargs):
        
        # Obtener la instancia de la habitación asociada a la reservación
        room = self.idRoom
        # Cambiar el atributo 'disponible' de la habitación a True
        room.disponible = True
        # Guardar la instancia de la habitación con el atributo actualizado
        room.save()
        # Llamar al método 'delete()' de la clase padre para eliminar la instancia de la reservación
        #factura=Reservacion.objects.filter(idUsuario=self.idUsuario,idRoom=self.idRoom,fechaDeInicio=self.fechaDeInicio,fechaDeFin=self.fechaDeFin)
        #for f in factura:
        # f.delete()
        super(Reservacion, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Reservations'
        

    def __str__(self):
        return self.name
