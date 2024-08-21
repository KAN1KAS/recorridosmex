from django.contrib import admin
from .models import Tours
from .models import Reserva

# Register your models here.

class AdministrarTours(admin.ModelAdmin):
    list_display=('id','nombre','estado')
    search_fields=('nombre','estado','ciudad')
    date_hierarchy ='created'
    list_filter =('created','estado')

admin.site.register(Tours, AdministrarTours)

class AdministrarReservas(admin.ModelAdmin):
    list_display = ('tour', 'usuario', 'lugares_reservados', 'precio_pagado', 'fecha_reserva','status')
    search_fields=('tour','usuario')
    list_display_links=('tour','usuario')#vinculos directos para poder acceder a los datos completos 
    ##date_hierarchy='fecha_reserva'#mostrar la fecha
    ##list_filter='fecha_reserva'
    #search_fields=('nombre','estado','ciudad')
    #date_hierarchy ='created'
    #list_filter =('fecha_reserva')

admin.site.register(Reserva, AdministrarReservas)