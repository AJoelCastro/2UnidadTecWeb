from django.db import models

# Create your models here.
class Cliente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    idCliente=models.PositiveIntegerField(unique=True) 
    apellidos=models.CharField(max_length=80)
    nombres=models.CharField(max_length=80) 
    direccion=models.CharField(max_length=100) 
    sexo=models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado=models.BooleanField() 
    def __str__(self): return self.apellidos