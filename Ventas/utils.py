from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf(request, venta_id):
    from .models import CabeceraVentas, DetalleVentas
    
    # Obtener la venta y sus detalles
    venta = CabeceraVentas.objects.get(pk=venta_id)
    detalles = DetalleVentas.objects.filter(idventa=venta)
    
    # Preparar el contexto para la plantilla
    context = {
        'venta': venta,
        'detalles': detalles,
        'empresa': 'SISTEMA DE VENTAS',
        'direccion': 'Av. Principal 123, Ciudad',
        'telefono': '(01) 123-4567',
        'email': 'info@sistemaventas.com',
    }
    
    # Generar el PDF
    pdf = render_to_pdf('venta/pdf_template.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Venta_{venta.nrodoc}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    
    return HttpResponse("Error al generar el PDF", status=400)