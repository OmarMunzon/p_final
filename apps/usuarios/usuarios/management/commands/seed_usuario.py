"""
Comando para poblar la base de datos con usuarios de prueba.
Uso: python manage.py seed_usuario
"""

from django.core.management.base import BaseCommand
from apps.usuarios.usuarios.models import Usuario, Estudiante, Profesor, PerfilEstudiante, PerfilProfesor


class Command(BaseCommand):
    help = "Pobla la base de datos con usuarios de prueba (estudiantes y profesores)"

    def handle(self, *args, **options):
        """
        Método principal que ejecuta la población de datos.
        """
        self.stdout.write(self.style.WARNING("🔄 Iniciando población de usuarios..."))

        # Limpiar datos existentes (opcional, comentar si deseas conservar)
        # Usuario.objects.all().delete()

        # Crear estudiantes
        self.crear_estudiantes()

        self.stdout.write(self.style.SUCCESS("✅ Población de usuarios completada exitosamente"))

    def crear_estudiantes(self):
        """Crea varios usuarios estudiantes con sus perfiles."""
        estudiantes_data = [            
            {
                "email": "maria.garcia@example.com",
                "nombre": "María",
                "apellido": "García",
                "password": "password123",
                "nivel": 2,
                "progreso": 78.00,
            },
            {
                "email": "carlos.lopez@example.com",
                "nombre": "Carlos",
                "apellido": "López",
                "password": "password123",
                "nivel": 1,
                "progreso": 20.00,
            },
            {
                "email": "ana.martinez@example.com",
                "nombre": "Ana",
                "apellido": "Martínez",
                "password": "password123",
                "nivel": 3,
                "progreso": 85.25,
            },
            {
                "email": "luis.rodriguez@example.com",
                "nombre": "Luis",
                "apellido": "Rodríguez",
                "password": "password123",
                "nivel": 2,
                "progreso": 55.00,
            },
        ]

        for datos in estudiantes_data:
            email = datos["email"]
            
            # Verificar si el usuario ya existe
            if Usuario.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f"⚠️  Estudiante {email} ya existe, omitiendo..."))
                continue

            # Crear usuario estudiante
            usuario = Estudiante.objects.create_user(
                email=email,
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                password=datos["password"],
            )

            # Crear perfil de estudiante
            PerfilEstudiante.objects.create(
                usuario=usuario,
                nivel_actual=datos["nivel"],
                progreso=datos["progreso"],
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Estudiante creado: {usuario.get_full_name()} "
                    f"(Nivel {datos['nivel']}, Progreso {datos['progreso']}%)"
                )
            )
    