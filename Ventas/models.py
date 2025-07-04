from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from Productos.models import Product
from Clientes.models import Cliente

# Create your models here.

class Tipo(models.Model):
    TIPO_CHOICES = [
        ('BOLETA', 'BOLETA'),
        ('FACTURA', 'FACTURA'),
    ]
    descripcion = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    def __str__(self):
        return self.descripcion

class Parametros(models.Model):
    idtipo = models.OneToOneField(Tipo, on_delete=models.CASCADE, primary_key=True)
    numeracion = models.CharField(max_length=15)
    serie = models.CharField(max_length=3)
    @classmethod
    def actualizar_numero(cls, idtipo, numeracion):
        try:
            with transaction.atomic():
                parametro = cls.objects.select_for_update().get(idtipo=idtipo)
                parametro.numeracion = numeracion
                parametro.save()
            return True
        except (Parametros.DoesNotExist, ValidationError) as e:
            return False
        except Exception as e:
            return False
        
    def __str__(self):
        return f"{self.serie}-{self.numeracion}"

class CabeceraVentas(models.Model):
    idcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    idtipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    estado=models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    nrodoc = models.CharField(max_length=12, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Venta {self.idventa} - {self.idcliente.nombres}"

class DetalleVentas(models.Model):
    idventa = models.ForeignKey(CabeceraVentas, on_delete=models.CASCADE)
    idproducto = models.ForeignKey(Product, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('idventa', 'idproducto')
    
    def __str__(self):
        return f"Detalle {self.idventa.idventa} - {self.idproducto.descripcion}"
