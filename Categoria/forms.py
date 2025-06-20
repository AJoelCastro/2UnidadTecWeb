from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [ 'descripcion', 'estado']
        labels = {
            'descripcion': 'Descripción',
            'estado': 'Estado'
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }