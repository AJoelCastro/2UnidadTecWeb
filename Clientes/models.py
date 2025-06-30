from django.db import models

# Create your models here.
class Cliente(models.Model):
    
    nombres=models.CharField(max_length=80)
    ruc_dni= models.CharField(max_length=11, unique=True)
    email= models.EmailField(blank=True, null=True) 
    direccion=models.CharField(max_length=100) 

    def __str__(self): return self.nombres