from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDay
from .models import CabeceraVentas, DetalleVentas, Tipo, Parametros
from Productos.models import Product
from .forms import VentaForm, DetalleVentaFormSet
import datetime
import json
from calendar import monthrange

def listar_venta(request):
    ventas = CabeceraVentas.objects.all()
    return render(request, 'venta/lista.html', {'ventas': ventas})

def dashboard(request):
    # Obtener el año y mes actual
    hoy = datetime.date.today()
    año_actual = hoy.year
    mes_actual = hoy.month
    
    # Obtener ventas del mes actual
    ventas_mes = CabeceraVentas.objects.filter(
        fecha_venta__year=año_actual,
        fecha_venta__month=mes_actual,
        estado=True
    )
    
    # Calcular total de ventas del mes
    total_ventas_mes = ventas_mes.aggregate(total=Sum('total'))['total'] or 0
    
    # Obtener cantidad de ventas del mes
    cantidad_ventas_mes = ventas_mes.count()
    
    # Obtener ventas por día del mes actual
    ventas_por_dia = CabeceraVentas.objects.filter(
        fecha_venta__year=año_actual,
        fecha_venta__month=mes_actual,
        estado=True
    ).annotate(
        dia=TruncDay('fecha_venta')
    ).values('dia').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('dia')
    
    # Preparar datos para gráficos
    dias = []
    totales = []
    cantidades = []
    
    # Obtener el número de días en el mes actual
    _, dias_en_mes = monthrange(año_actual, mes_actual)
    
    # Inicializar arrays con ceros para todos los días del mes
    for dia in range(1, dias_en_mes + 1):
        dias.append(dia)
        totales.append(0)
        cantidades.append(0)
    
    # Llenar con datos reales
    for venta in ventas_por_dia:
        dia = venta['dia'].day - 1  # Índice 0-based
        totales[dia] = float(venta['total'])
        cantidades[dia] = venta['cantidad']
    
    # Obtener productos más vendidos
    productos_vendidos = DetalleVentas.objects.filter(
        idventa__fecha_venta__year=año_actual,
        idventa__fecha_venta__month=mes_actual,
        idventa__estado=True
    ).values(
        'idproducto__description'
    ).annotate(
        cantidad=Sum('cantidad')
    ).order_by('-cantidad')[:5]
    
    # Preparar datos para gráfico de productos
    nombres_productos = [p['idproducto__description'] for p in productos_vendidos]
    cantidades_productos = [float(p['cantidad']) for p in productos_vendidos]
    
    # Obtener ventas totales (histórico)
    total_ventas_historico = CabeceraVentas.objects.filter(estado=True).aggregate(total=Sum('total'))['total'] or 0
    cantidad_ventas_historico = CabeceraVentas.objects.filter(estado=True).count()
    
    # Obtener ventas por mes (para gráfico anual)
    ventas_por_mes = CabeceraVentas.objects.filter(
        fecha_venta__year=año_actual,
        estado=True
    ).annotate(
        mes=TruncMonth('fecha_venta')
    ).values('mes').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('mes')
    
    # Preparar datos para gráfico anual
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    totales_por_mes = [0] * 12
    cantidades_por_mes = [0] * 12
    
    for venta in ventas_por_mes:
        mes = venta['mes'].month - 1  # Índice 0-based
        totales_por_mes[mes] = float(venta['total'])
        cantidades_por_mes[mes] = venta['cantidad']
    
    # Productos con stock bajo (menos de 5 unidades)
    productos_stock_bajo = Product.objects.filter(stock__lt=5, stock__gt=0).order_by('stock')
    
    # Productos sin stock
    productos_sin_stock = Product.objects.filter(stock__lte=0)
    
    context = {
        'total_ventas_mes': total_ventas_mes,
        'cantidad_ventas_mes': cantidad_ventas_mes,
        'total_ventas_historico': total_ventas_historico,
        'cantidad_ventas_historico': cantidad_ventas_historico,
        'dias': json.dumps(dias),
        'totales': json.dumps(totales),
        'cantidades': json.dumps(cantidades),
        'nombres_productos': json.dumps(nombres_productos),
        'cantidades_productos': json.dumps(cantidades_productos),
        'meses': json.dumps(meses),
        'totales_por_mes': json.dumps(totales_por_mes),
        'cantidades_por_mes': json.dumps(cantidades_por_mes),
        'productos_stock_bajo': productos_stock_bajo,
        'productos_sin_stock': productos_sin_stock,
        'mes_actual': meses[mes_actual - 1],
        'año_actual': año_actual
    }
    
    return render(request, 'venta/dashboard.html', context)

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
                    
                    # Actualizar estado del producto si el stock llega a cero
                    if producto.stock <= 0:
                        producto.status = False
                    
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
                # Si el producto estaba inactivo pero ahora tiene stock, activarlo
                if producto.stock > 0:
                    producto.status = True
                producto.save()
            
            # Verificar stock disponible antes de procesar la venta
            stock_suficiente = True
            productos_sin_stock = []
            
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    producto = form.cleaned_data['idproducto']
                    cantidad = form.cleaned_data['cantidad']
                    
                    # Verificar si el producto tiene stock suficiente
                    if producto.stock < float(cantidad):
                        stock_suficiente = False
                        productos_sin_stock.append(f"{producto.description} (Stock: {producto.stock})")
            
            if not stock_suficiente:
                # Restaurar el estado original de los productos
                for detalle in detalles_antiguos:
                    producto = detalle.idproducto
                    producto.stock -= float(detalle.cantidad)
                    if producto.stock <= 0:
                        producto.status = False
                    producto.save()
                
                mensaje_error = 'No se puede actualizar la venta. Los siguientes productos no tienen stock suficiente: '
                mensaje_error += ', '.join(productos_sin_stock)
                messages.error(request, mensaje_error)
                return render(request, 'venta/form.html', {
                    'form': form,
                    'formset': formset,
                    'action': 'Editar'
                })
            
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
                    # Actualizar estado del producto si el stock llega a cero
                    if producto.stock <= 0:
                        producto.status = False
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
            
            # Si el producto estaba inactivo pero ahora tiene stock, activarlo
            if producto.stock > 0:
                producto.status = True
                
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