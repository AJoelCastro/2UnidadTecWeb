from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import CabeceraVentas, DetalleVentas, Tipo, Parametros
from Productos.models import Product
from .forms import VentaForm, DetalleVentaFormSet
import datetime

def listar_venta(request):
    ventas = CabeceraVentas.objects.all()
    return render(request, 'venta/lista.html', {'ventas': ventas})

@transaction.atomic
def agregar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            # Guardar la cabecera
            venta = form.save(commit=False)
            
            # Actualizar numeración del documento
            tipo = venta.idtipo
            parametro = get_object_or_404(Parametros, idtipo=tipo)
            
            # Usar la serie del parámetro en lugar de crear una nueva
            serie = parametro.serie
            nueva_numeracion = str(int(parametro.numeracion) + 1).zfill(8)
            venta.nrodoc = f"{serie}-{nueva_numeracion}"
            
            venta.save()
            
            # Guardar los detalles
            formset.instance = venta
            formset.save()
            
            # Actualizar el número de documento en parámetros
            Parametros.actualizar_numero(tipo.id, nueva_numeracion)
            
            # Actualizar stock de productos
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    producto = form.cleaned_data['idproducto']
                    cantidad = form.cleaned_data['cantidad']
                    # Convertir Decimal a float antes de la operación
                    producto.stock -= float(cantidad)
                    producto.save()
            
            messages.success(request, 'Venta registrada correctamente')
            
            # Redirigir a la generación del PDF
            return redirect('generar_pdf', venta_id=venta.id)
    else:
        form = VentaForm(initial={'fecha_venta': datetime.date.today()})
        formset = DetalleVentaFormSet()
    
    return render(request, 'venta/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Crear'
    })

@transaction.atomic
def editar_venta(request, pk):
    venta = get_object_or_404(CabeceraVentas, pk=pk)
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = DetalleVentaFormSet(request.POST, instance=venta)
        
        if form.is_valid() and formset.is_valid():
            # Restaurar stock de productos antes de actualizar
            detalles_antiguos = DetalleVentas.objects.filter(idventa=venta)
            for detalle in detalles_antiguos:
                producto = detalle.idproducto
                # Convertir Decimal a float antes de la operación
                producto.stock += float(detalle.cantidad)
                producto.save()
            
            # Guardar la cabecera y detalles actualizados
            form.save()
            formset.save()
            
            # Actualizar stock con los nuevos valores
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    producto = form.cleaned_data['idproducto']
                    cantidad = form.cleaned_data['cantidad']
                    # Convertir Decimal a float antes de la operación
                    producto.stock -= float(cantidad)
                    producto.save()
            
            messages.success(request, 'Venta actualizada correctamente')
            return redirect('listar_venta')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleVentaFormSet(instance=venta)
    
    return render(request, 'venta/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Editar'
    })

@transaction.atomic
def anular_venta(request, pk):
    venta = get_object_or_404(CabeceraVentas, pk=pk)
    
    if request.method == 'POST':
        # Restaurar stock de productos
        detalles = DetalleVentas.objects.filter(idventa=venta)
        for detalle in detalles:
            producto = detalle.idproducto
            # Convertir Decimal a float antes de la operación
            producto.stock += float(detalle.cantidad)
            producto.save()
        
        # Anular la venta (cambiar estado)
        venta.estado = False
        venta.save()
        
        messages.success(request, 'Venta anulada correctamente')
        return redirect('listar_venta')
    
    return render(request, 'venta/confirmar_anulacion.html', {'venta': venta})

# API para obtener información del producto
def get_producto_info(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Product.objects.get(pk=producto_id)
        return JsonResponse({
            'precio': producto.price,
            'stock': producto.stock
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

# API para obtener información de la serie según el tipo
def get_serie_info(request):
    tipo_id = request.GET.get('tipo_id')
    try:
        parametro = Parametros.objects.get(idtipo=tipo_id)
        return JsonResponse({
            'serie': parametro.serie,
            'numeracion': parametro.numeracion
        })
    except Parametros.DoesNotExist:
        return JsonResponse({'error': 'Parámetro no encontrado'}, status=404)