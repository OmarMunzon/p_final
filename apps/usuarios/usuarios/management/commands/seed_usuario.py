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
                "email": "maria.garcia@gmail.com",
                "nombre": "María",
                "apellido": "García",
                "password": "passwordUser123",
                "rol": "estudiante",                
                "nivel": 1,
                "progreso": 0.00,
            },
            {
                "email": "carlos.lopez@gmail.com",
                "nombre": "Carlos",
                "apellido": "López",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00,
            },
            {
                "email": "ana.martinez@gmail.com",
                "nombre": "Ana",
                "apellido": "Martínez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00,
            },
            {
                "email": "luis.rodriguez@gmail.com",
                "nombre": "Luis",
                "apellido": "Rodríguez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00,
            },
            {
                "email": "diego.fernandez@gmail.com",
                "nombre": "Diego",
                "apellido": "Fernández",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "lucia.sanchez@gmail.com",
                "nombre": "Lucía",
                "apellido": "Sánchez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "javier.perez@gmail.com",
                "nombre": "Javier",
                "apellido": "Pérez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "valeria.diaz@gmail.com",
                "nombre": "Valeria",
                "apellido": "Díaz",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "alejandro.torres@gmail.com",
                "nombre": "Alejandro",
                "apellido": "Torres",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "elena.ramirez@gmail.com",
                "nombre": "Elena",
                "apellido": "Ramírez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "mateo.castro@gmail.com",
                "nombre": "Mateo",
                "apellido": "Castro",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "camila.morales@gmail.com",
                "nombre": "Camila",
                "apellido": "Morales",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "nicolas.herrera@gmail.com",
                "nombre": "Nicolás",
                "apellido": "Herrera",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "martina.ruiz@gmail.com",
                "nombre": "Martina",
                "apellido": "Ruiz",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "sebastian.castillo@gmail.com",
                "nombre": "Sebastián",
                "apellido": "Castillo",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "isabella.gutierrez@gmail.com",
                "nombre": "Isabella",
                "apellido": "Gutiérrez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "matias.flores@gmail.com",
                "nombre": "Matías",
                "apellido": "Flores",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "natalia.acosta@gmail.com",
                "nombre": "Natalia",
                "apellido": "Acosta",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "daniel.ortiz@gmail.com",
                "nombre": "Daniel",
                "apellido": "Ortiz",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "gabriela.silva@gmail.com",
                "nombre": "Gabriela",
                "apellido": "Silva",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "tomas.mendoza@gmail.com",
                "nombre": "Tomás",
                "apellido": "Mendoza",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },            
            {
                "email": "valentina.vargas@gmail.com",
                "nombre": "Valentina",
                "apellido": "Vargas",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "lucas.ibanez@gmail.com",
                "nombre": "Lucas",
                "apellido": "Ibáñez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "mariana.rios@gmail.com",
                "nombre": "Mariana",
                "apellido": "Ríos",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "benjamin.medina@gmail.com",
                "nombre": "Benjamín",
                "apellido": "Medina",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "victoria.campos@gmail.com",
                "nombre": "Victoria",
                "apellido": "Campos",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "emiliano.vega@gmail.com",
                "nombre": "Emiliano",
                "apellido": "Vega",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "juliana.fuentes@gmail.com",
                "nombre": "Juliana",
                "apellido": "Fuentes",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "joaquin.marquez@gmail.com",
                "nombre": "Joaquín",
                "apellido": "Márquez",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "daniela.reyes@gmail.com",
                "nombre": "Daniela",
                "apellido": "Reyes",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
            },
            {
                "email": "samuel.miranda@gmail.com",
                "nombre": "Samuel",
                "apellido": "Miranda",
                "password": "passwordUser123",
                "rol": "estudiante",
                "nivel": 1,
                "progreso": 0.00
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
                rol=datos["rol"],
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
    