from django.shortcuts import render
from .models import Categoria

def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/lista.html', {'categorias': categorias})