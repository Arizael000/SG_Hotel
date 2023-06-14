from django.db import models

# Create your models here.




class Hotel(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Hotels'
              
    def __str__(self):
        return self.nombre
    
