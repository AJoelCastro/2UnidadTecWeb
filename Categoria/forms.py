from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['idCategoria', 'descripcion', 'estado']
        labels = {
            'idCategoria': 'ID',
            'descripcion': 'Descripción',
            'estado': 'Estado'
        }
        widgets = {
            'idCategoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }