# Generated by Django 4.2.1 on 2023-06-06 13:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='El CI debe tener 11 dígitos', regex='^[0-9]{11}$')])),
                ('phone', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe comenzar con 5 y tener 8 dígitos', regex='^5[0-9]{7}$')])),
                ('adress', models.CharField(max_length=30)),
                ('bio', models.TextField(max_length=500)),
                ('usuarioRelacionado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
