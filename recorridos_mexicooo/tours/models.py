from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tours(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    km = models.CharField(max_length=20)
    tiempo_estimado = models.CharField(max_length=50)
    punto_inicio = models.CharField(max_length=100)
    punto_final = models.CharField(max_length=100)
    costo = models.FloatField()
    ganancias = models.FloatField(null=True)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    imagen = models.ImageField(null=True,upload_to="fotos")
    lugares_disponibles = models.IntegerField()
    created= models.DateField(auto_now_add=True, verbose_name="fecha creación")
    mapa = models.TextField()

    class Meta:
        verbose_name= "Tour"
        verbose_name_plural = "Tours"
        ordering = ["id"]

    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    STATUS_CHOICES = [
        ('1', 'Activo'),
        ('0', 'Cancelada'),
    ]
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    lugares_reservados = models.IntegerField()
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'Reserva de {self.usuario} para el tour {self.tour}'
        #return self.tour

