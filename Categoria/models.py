from django.db import models

# Create your models here.
class Categoria(models.Model):
    descripcion=models.CharField(max_length=30) 
    estado=models.BooleanField() 
    def __str__(self): 
        return self.descripcion