from django.shortcuts import render
from django.contrib.auth import authenticate, login as login_auth,logout
from django.contrib.auth.models import User # Extraer el modelo de usuarios DJANGO 
from django.contrib import messages
from usuarios.models import Usuarios,Perfil
from django.shortcuts import render, redirect
from .forms import LoginForm,PerfilForm
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() #Saving form user data in the model
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_auth(request, user)#Autenticar usuario automaticamente
                return redirect('principal')  # Redirigir a la página principal
        else:
            print(form.errors)  # mostrar los errores en la consola
            
    else:
        form = UserCreationForm()
    return render(request,"inicio/cuenta/registro.html",{"form":form})

def login(request):
    if request.user.is_authenticated:
        return redirect('principal')  # Redirige a la página principal si ya está autenticado
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['contraseña']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect('principal')  # Redirige a la página principal o donde quieras
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos.'
            return render(request, 'inicio/cuenta/login.html', {'error_message': error_message})
    return render(request, 'inicio/cuenta/login.html')

@login_required
def cuenta(request):
    usuario = request.user #obtiene el usuario que esta en sesion
    try:
        datos=Perfil.objects.get(user=usuario)
    except Perfil.DoesNotExist:

        datos = Perfil(user=usuario)  # Crea un nuevo perfil asociado al usuario
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=datos)  # Carga los datos del perfil en el formulario
        if form.is_valid():
            form.save()  # Guarda el perfil asociado al usuario
            messages.success(request, 'Perfil actualizado exitosamente.')  # Mensaje de éxito
            return redirect('cuenta')  # Redirige a la página del perfil u otra que prefieras
        else:
            messages.error(request, 'Hubo un error al guardar el perfil. Por favor, revisa los datos ingresados.')  # Mensaje de error
    else:
        form = PerfilForm(instance=datos)  # Prellena el formulario con los datos del perfil existente
    return render(request, 'inicio/cuenta/perfil.html',{"usuario":datos})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('principal')

