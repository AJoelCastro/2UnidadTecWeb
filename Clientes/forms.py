from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [ 'nombres', 'ruc_dni', 'email', 'direccion']
        labels = {
            'nombres': 'Nombres',
            'ruc_dni': 'RUC/DNI',
            'email': 'Email',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc_dni': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }