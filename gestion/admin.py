from django.contrib import admin

from .models import Cliente, Cuenta, Transaccion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono")
    search_fields = ("nombre", "email", "telefono")

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente",)
    search_fields = ("cliente__nombre",)
    filter_horizontal = ("contactos_autorizados",)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("cuenta", "tipo", "monto", "descripcion", "fecha",)
    search_fields = ("cuenta__numero", "tipo", "fecha",)
    list_filter = ("tipo",)