from django.contrib import admin
from .models import Usuarios
from .models import Perfil

# Register your models here.
class AdministrarUsuarios(admin.ModelAdmin):
    list_display=('nombre','estado')
    search_fields=('nombre','estado','ciudad')
    date_hierarchy ='created'
    list_filter =('created','estado')
admin.site.register(Usuarios, AdministrarUsuarios) 

class AdministrarPerfil(admin.ModelAdmin):
    list_display=('user','nombre','apellidos','telefono','correo','estado','ciudad')
    search_fields=('nombre','estado','ciudad')
    #date_hierarchy ='created'
    #list_filter =('created','estado')
admin.site.register(Perfil, AdministrarPerfil) 

