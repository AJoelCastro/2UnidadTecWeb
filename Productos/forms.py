from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['idProduct', 'description', 'idCategoria', 'price', 'stock', 'status']
        labels = {
            'idProduct': 'ID',
            'description': 'Descripción',
            'idCategoria': 'Categoría',
            'price': 'Precio',
            'stock': 'Stock',
            'status': 'Estado'
        }
        widgets = {
            'idProduct': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }