from django.contrib import admin
from .models import Tipo 
from .models import Parametro

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('tipo_id', 'descripcion')
    
    def cargar_datos_iniciales(self, request, queryset):
        # Crear registros iniciales si no existen
        if not Tipo.objects.filter(tipo_id=1).exists():
            Tipo.objects.create(tipo_id=1, descripcion='FACTURA')
        if not Tipo.objects.filter(tipo_id=2).exists():
            Tipo.objects.create(tipo_id=2, descripcion='BOLETA')
        self.message_user(request, "Datos iniciales cargados exitosamente")
    
    cargar_datos_iniciales.short_description = "Cargar datos iniciales (FACTURA/BOLETA)"
    actions = [cargar_datos_iniciales]

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ('tipo_id', 'numeracion', 'serie')
    ordering = ('tipo_id',)
    
    def cargar_datos_iniciales(self, request, queryset):
        # Crear o actualizar registros iniciales
        Parametro.objects.update_or_create(
            tipo_id=1,
            defaults={'numeracion': '00010', 'serie': '001'}
        )
        Parametro.objects.update_or_create(
            tipo_id=2,
            defaults={'numeracion': '01000', 'serie': '002'}
        )
        self.message_user(request, "Datos iniciales cargados exitosamente")
    
    cargar_datos_iniciales.short_description = "Cargar datos iniciales (FACTURA/BOLETA)"
    actions = [cargar_datos_iniciales]