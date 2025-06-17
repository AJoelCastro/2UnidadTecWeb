from django.db import models
from Categoria.models import Categoria
# Create your models here.
class Product(models.Model):
    idProduct = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=50)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    stock = models.FloatField(blank=True, null=True)
    status = models.BooleanField()

    def __str__(self):
        
        return self.description