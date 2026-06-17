"""
Vistas del módulo de usuarios.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FormularioLogin, FormularioRegistro
from .models import PerfilEstudiante, PerfilProfesor

def vista_registro(request):
    """Vista para registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    if request.method == "POST":
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            print("resultado ",usuario)
            login(request, usuario)
            messages.success(
                request,
                f"¡Bienvenido, {usuario.get_full_name()}! "
                "Tu cuenta fue creada exitosamente.",
            )
            return redirect("usuarios:dashboard")
        else:
            messages.error(
                request,
                "Por favor corrige los errores del formulario.",
            )
    else:
        formulario = FormularioRegistro()

    contexto = {"formulario": formulario, "titulo": "Registro"}
    return render(request, "usuarios/registro.html", contexto)


def vista_login(request):
    """Vista para inicio de sesión."""
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    if request.method == "POST":
        formulario = FormularioLogin(request.POST)
        if formulario.is_valid():
            usuario = formulario.usuario_autenticado
            login(request, usuario)
            messages.success(
                request,
                f"¡Bienvenido de nuevo, {usuario.get_full_name()}!",
            )
            siguiente = request.GET.get("next", "usuarios:dashboard")
            return redirect(siguiente)
        else:
            messages.error(
                request,
                "Credenciales incorrectas. Inténtalo de nuevo.",
            )
    else:
        formulario = FormularioLogin()

    contexto = {"formulario": formulario, "titulo": "Iniciar Sesión"}
    return render(request, "usuarios/login.html", contexto)


def vista_logout(request):
    """Vista para cerrar sesión."""
    if request.method == "POST":
        logout(request)
        messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("usuarios:login")


@login_required
def vista_dashboard(request):
    """Vista del panel principal adaptada a Estudiantes y Profesores."""
    usuario = request.user
    contexto = {
        "titulo": "Dashboard",
        "usuario": usuario,
    }

    # 1. SI ES ESTUDIANTE
    if usuario.rol == 'estudiante':
        estudiante = PerfilEstudiante.objects.filter(usuario=usuario).first()
        mi_nivel = "principiante"
        
        if estudiante:
            match estudiante.nivel_actual:
                case 1: mi_nivel = "principiante"
                case 2: mi_nivel = "intermedio"
                case 3: mi_nivel = "avanzado"
                
        contexto.update({
            "estudiante": estudiante,
            "mi_nivel": mi_nivel,
        })
        return render(request, "usuarios/dashboard.html", contexto)

    # 2. SI ES PROFESOR
    elif usuario.rol == 'profesor':
        profesor = PerfilProfesor.objects.filter(usuario=usuario).first()
        
        contexto.update({
            "profesor": profesor,
        })
        return render(request, "usuarios/dashboard.html", contexto)
        
    # 3. CASO DE EMERGENCIA (Por si creas un usuario desde el admin sin rol)
    else:
        messages.error(request, "Tu cuenta no tiene un rol asignado.")
        return redirect("usuarios:login")