from django.shortcuts import render
from .models import Cliente

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/lista.html', {'clientes': clientes})