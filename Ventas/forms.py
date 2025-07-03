from django import forms
from .models import CabeceraVentas, DetalleVentas, Tipo
from Clientes.models import Cliente
from Productos.models import Product
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = CabeceraVentas
        fields = ['idcliente', 'fecha_venta', 'idtipo', 'nrodoc', 'subtotal', 'igv', 'total']
        labels = {
            'idcliente': 'Cliente',
            'fecha_venta': 'Fecha de Venta',
            'idtipo': 'Tipo de Documento',
            'nrodoc': 'Número de Documento',
            'subtotal': 'Subtotal',
            'igv': 'IGV',
            'total': 'Total'
        }
        widgets = {
            'idcliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_venta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'idtipo': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_documento'}),
            'nrodoc': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'igv': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }
        
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        # Hacer que el campo nrodoc no sea requerido
        self.fields['nrodoc'].required = False

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVentas
        fields = ['idproducto', 'precio', 'cantidad']
        labels = {
            'idproducto': 'Producto',
            'precio': 'Precio',
            'cantidad': 'Cantidad'
        }
        widgets = {
            'idproducto': forms.Select(attrs={'class': 'form-control select-producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control precio', 'readonly': 'readonly'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad', 'min': '1'})
        }

# Creamos un formset para manejar múltiples detalles de venta
DetalleVentaFormSet = inlineformset_factory(
    CabeceraVentas, 
    DetalleVentas,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True
)