from django.db import models

# Create your models here.
class Tipo(models.Model):
    tipo_id = models.AutoField(primary_key=True, verbose_name='ID')
    descripcion = models.CharField(max_length=20)
    
    def __str__(self):
        return self.descripcion
    
class Parametro(models.Model):
    tipo_id = models.IntegerField(primary_key=True, verbose_name='Tipo ID')
    numeracion = models.CharField(max_length=15)
    serie = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.tipo_id} - {self.serie}{self.numeracion}"    