from django.shortcuts import render, get_object_or_404, redirect
from .models import Tours, Reserva
from usuarios.models import Perfil,Usuarios
from .forms import ReservaForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
from datetime import datetime



# Create your views here.

    

def tours(request):
    #tour_id = get_object_or_404(Tours, id=id)
    hoy = date.today()
    tours = Tours.objects.filter(fecha__gt=hoy)
    return render(request,"tours/tours.html",{"tours":tours})

def catalogos(request):
    return render(request,"tours/catalogos.html")

def mich(request):
    hoy = date.today()
    tours = Tours.objects.filter(estado="Michoacán", fecha__gt=hoy)
    return render(request,"tours/estados/michoacan/mich.html",{"tours":tours})

def gto(request):
    hoy = date.today()
    tours = Tours.objects.filter(estado="Guanajuato", fecha__gt=hoy)
    return render(request,"tours/estados/guanajuato/gto.html",{"tours":tours})

def qro(request):
    hoy = date.today()
    tours = Tours.objects.filter(estado="Querétaro", fecha__gt=hoy)
    return render(request,"tours/estados/queretaro/qro.html",{"tours":tours})

def edomx(request):
    hoy = date.today()
    tours = Tours.objects.filter(estado="Estado de México", fecha__gt=hoy)
    return render(request,"tours/estados/EdoMex/edomx.html",{"tours":tours})

def vcruz(request):
    hoy = date.today()
    tours = Tours.objects.filter(estado="Veracruz", fecha__gt=hoy)
    return render(request,"tours/estados/veracruz/vcruz.html",{"tours":tours})

def realizados(request):
    hoy = date.today()
    tours = Tours.objects.filter(fecha__lt=hoy)
    return render(request,"tours/realizados.html",{"tours":tours})

# def detalle_tour(request, id):
#     tours = get_object_or_404(Tours, pk=id)
#     return render(request, 'tours/detalles.html', {'tours': tours})


def detalle_tour(request, id):
    tour = get_object_or_404(Tours, id=id)  # Obtén el tour o devuelve un 404 si no existe
    usuario = request.user  # Obtén el usuario que está en sesión

    # Verifica si el tour ya ha pasado
    ahora = timezone.now()
    tour_fecha_hora = timezone.make_aware(datetime.combine(tour.fecha, tour.hora))
    tour_vencido = tour_fecha_hora < ahora

    if request.method == 'POST' and not tour_vencido:
        form = ReservaForm(request.POST)
        if form.is_valid():
            lugares_reservados = form.cleaned_data['lugares_reservados']
            
            # Evitar la reserva de lugares negativos o superiores a los disponibles
            if lugares_reservados <= 0 or lugares_reservados > tour.lugares_disponibles:
                messages.error(request, 'La cantidad de lugares reservados no es válida.')
            else:
                with transaction.atomic():  # Para asegurar que la operación es atómica
                    reserva = form.save(commit=False)  # No guardes aún la reserva
                    reserva.tour = tour  # Asocia la reserva con el tour
                    reserva.usuario = usuario  # Asocia la reserva con el usuario en sesión
                    reserva.precio_pagado = lugares_reservados * tour.costo  # Calcula el costo total
                    reserva.save()  # Guarda la reserva en la base de datos

                    # Actualizar lugares disponibles y ganancias del tour
                    tour.lugares_disponibles -= lugares_reservados
                    tour.ganancias = (tour.ganancias or 0) + reserva.precio_pagado  # Sumar la nueva reserva a las ganancias existentes
                    tour.save()

                # Obtener el correo del usuario desde el perfil
                perfil = Perfil.objects.get(user=usuario)
                correo = perfil.correo

                # Enviar la factura al correo del usuario
                asunto = f'Factura de Compra - {tour.nombre}'
                mensaje = f"""
                Hola {perfil.nombre},

                Gracias por reservar con nosotros. Aquí tienes los detalles de tu reserva:

                Tour: {tour.nombre}
                Ciudad: {tour.ciudad}
                Estado: {tour.estado}
                Fecha: {tour.fecha}
                Hora: {tour.hora}
                Kilómetros del recorrido: {tour.km}
                Punto de inicio: {tour.punto_inicio}
                Punto final: {tour.punto_final}
                Lugares reservados: {reserva.lugares_reservados}
                Costo total: ${reserva.precio_pagado}

                Esperamos que disfrutes del tour.

                Saludos,
                Equipo de Tours
                """
                send_mail(asunto, mensaje, 'martillo070@mail.com', [correo])

                messages.success(request, '¡Tu reserva ha sido registrada exitosamente! La factura ha sido enviada a tu correo.')
                return redirect(reverse('reserva_detalle', args=[reserva.id]))
        else:
            messages.error(request, 'Hubo un error con tu reserva. Por favor, revisa los datos e inténtalo de nuevo.')
            print(form.errors)
    else:
        form = ReservaForm()  # Inicializa el formulario vacío para GET requests

    # Obtén todas las reservas activas para el tour
    reservas = Reserva.objects.filter(tour=tour, status='1').select_related('usuario')

    # Obtén los perfiles asociados a las reservas
    perfiles = Perfil.objects.filter(user__in=[reserva.usuario for reserva in reservas])

    return render(request, 'tours/detalles.html', {
        'form': form,
        'tours': tour,
        'perfiles': perfiles,
        'tour_vencido': tour_vencido,  # Añade esta variable al contexto
    })

def reserva_detalle(request,id):
    reserva = get_object_or_404(Reserva, id=id)
    return render(request, 'tours/reserva_detalle.html', {'reserva': reserva})

def mis_reservas(request):
    usuario = request.user
    reservas = Reserva.objects.filter(usuario=usuario).select_related('tour')
    return render(request, 'tours/mis_reservas.html', {'reservas': reservas})


