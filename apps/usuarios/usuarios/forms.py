"""
Formularios del módulo de usuarios.
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class FormularioRegistro(UserCreationForm):
    """Formulario para registro de nuevos usuarios."""

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com",
            }
        ),
    )
    nombre = forms.CharField(
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Tu nombre",
            }
        ),
    )
    apellido = forms.CharField(
        label="Apellido",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Tu apellido",
            }
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "••••••••",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "••••••••",
            }
        ),
    )

    class Meta:
        model = Usuario
        fields = ("email", "nombre", "apellido", "password1", "password2")

    def clean_email(self):
        """Valida que el email no esté registrado."""
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email


class FormularioLogin(forms.Form):
    """Formulario para inicio de sesión."""

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "••••••••",
            }
        ),
    )

    def clean(self):
        """Valida las credenciales del usuario."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            usuario = authenticate(username=email, password=password)
            if usuario is None:
                raise forms.ValidationError(
                    "Credenciales incorrectas. " "Verifique su email y contraseña."
                )
            if not usuario.es_activo:
                raise forms.ValidationError(
                    "Su cuenta está desactivada. " "Contacte al administrador."
                )
            self.usuario_autenticado = usuario

        return cleaned_data
