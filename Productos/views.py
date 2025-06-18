from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def producto_list(request):
    productos = Product.objects.all()
    return render(request, 'producto/lista.html', {'productos': productos})

def producto_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente')
            return redirect('producto_list')
    else:
        form = ProductForm()
    return render(request, 'producto/form.html', {'form': form, 'action': 'Crear'})

def producto_update(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente')
            return redirect('producto_list')
    else:
        form = ProductForm(instance=producto)
    return render(request, 'producto/form.html', {'form': form, 'action': 'Editar'})

def producto_delete(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente')
        return redirect('producto_list')
    return render(request, 'producto/confirm_delete.html', {'producto': producto})