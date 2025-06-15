from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from .forms import CategoriaForm

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_categorias')
    return render(request, 'categorias/formulario.html', {'form': form})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, idcategoria=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('lista_categorias')
    return render(request, 'categorias/formulario.html', {'form': form})

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, idcategoria=id)
    if request.method == "POST":
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})
