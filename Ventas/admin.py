from django.contrib import admin
from .models import Tipo, Parametros, CabeceraVentas, DetalleVentas

# Register your models here.
class ParametrosInline(admin.TabularInline):
    model = Parametros
    extra = 0

class TipoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    inlines = [ParametrosInline]

class DetalleVentasInline(admin.TabularInline):
    model = DetalleVentas
    extra = 0

class CabeceraVentasAdmin(admin.ModelAdmin):
    list_display = ('nrodoc', 'idcliente', 'fecha_venta', 'total', 'estado')
    list_filter = ('fecha_venta', 'estado', 'idtipo')
    search_fields = ('nrodoc', 'idcliente__nombres')
    date_hierarchy = 'fecha_venta'
    inlines = [DetalleVentasInline]

admin.site.register(Tipo, TipoAdmin)
admin.site.register(CabeceraVentas, CabeceraVentasAdmin)
