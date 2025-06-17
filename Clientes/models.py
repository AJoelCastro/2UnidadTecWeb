from django.db import models

# Create your models here.
class Categoria(models.Model):
    idCliente=models.PositiveIntegerField(unique=True) 
    apellidos=models.CharField(max_length=80)
    nombres=models.CharField(max_length=80) 
    direccion=models.CharField(max_length=100) 
    sexo=models.CharField(max_length=1)
    estado=models.BooleanField() 
    def __str__(self): return self.idCategoria