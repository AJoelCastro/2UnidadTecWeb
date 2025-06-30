from django.db import models
from Clientes.models import Cliente
from Productos.models import Product
from core.models import Tipo
from django.utils import timezone
# Create your models here.
class CabeceraVenta(models.Model):
    cliente      = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo         = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    fecha_venta  = models.DateField(default=timezone.now)
    nrodoc       = models.CharField(max_length=20)
    subtotal     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igv          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado       = models.BooleanField(default=True)

class DetalleVenta(models.Model):
    venta     = models.ForeignKey(CabeceraVenta, related_name="detalles", on_delete=models.CASCADE)
    producto  = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad  = models.PositiveIntegerField()
    precio    = models.DecimalField(max_digits=10, decimal_places=2)
