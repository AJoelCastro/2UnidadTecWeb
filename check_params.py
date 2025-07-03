# Script para verificar los parámetros

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto1.settings')
django.setup()

from Ventas.models import Tipo, Parametros

print('Detalles de Parámetros:')
for p in Parametros.objects.all():
    print(f'Tipo: {p.idtipo.descripcion}, Serie: {p.serie}, Numeración: {p.numeracion}')