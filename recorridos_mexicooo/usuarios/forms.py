from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuarios,Perfil

class LoginForm(forms.Form):
    user = forms.CharField(label="nombre", max_length=254, widget=forms.TextInput(attrs={
        'placeholder': 'CORREO',
        'id': 'nombre'
    }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'placeholder': 'CONTRASEÑA',
        'id': 'contraseña'
    }))

class RegistrarDatosForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['nombre', 'correo', 'estado', 'ciudad', 'contraseña', 'imagen']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre','apellidos', 'correo', 'telefono', 'estado','ciudad']
