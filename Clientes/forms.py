from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [ 'nombres', 'apellidos', 'direccion', 'sexo', 'estado']
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'direccion': 'Dirección',
            'sexo': 'Sexo',
            'estado': 'Estado'
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }