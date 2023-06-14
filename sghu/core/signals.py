from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def asignar_grupo_nuevo_usuario(sender, instance, created, **kwargs):
    if created:
        grupo = Group.objects.get(name='Clientes')
        instance.groups.add(grupo)
        
        
        
        
        