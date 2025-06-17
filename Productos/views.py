from django.shortcuts import render
from .models import Product

def producto_list(request):
    productos = Product.objects.all()
    return render(request, 'producto/lista.html', {'productos': productos})