# Django + PostgreSQL — Proyecto Base

Proyecto - Django estructurado con módulo de usuarios, autenticación y PostgreSQL.

## Requisitos previos

- Python
- PostgreSQL 14+
- pip

## Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd <nombre-proyecto>

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales reales

# 5. Crear la base de datos en PostgreSQL
psql -U postgres -c "CREATE DATABASE mi_proyecto_db;"

# 6. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 7. Crear superusuario
python manage.py createsuperuser

# 8. Ejecutar el servidor
python manage.py runserver
```

## Estructura del proyecto

```
.
├── apps/
│   └── usuarios/           # Módulo de usuarios
│       ├── migrations/
│       ├── templates/
│       │   └── usuarios/
│       │       ├── base.html
│       │       ├── registro.html
│       │       ├── login.html
│       │       └── dashboard.html
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── managers.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/
├── .env                    # No subir a Git
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## URLs disponibles

| Ruta            | Descripción              |
|-----------------|--------------------------|
| `/registro/`    | Registro de usuario      |
| `/login/`       | Inicio de sesión         |
| `/logout/`      | Cerrar sesión            |
| `/dashboard/`   | Panel principal          |
| `/admin/`       | Panel de administración  |

## Variables de entorno (.env)

| Variable      | Descripción                    |
|---------------|--------------------------------|
| `SECRET_KEY`  | Clave secreta de Django        |
| `DEBUG`       | Modo debug (`True`/`False`)    |
| `ALLOWED_HOSTS` | Hosts permitidos             |
| `DB_NAME`     | Nombre de la base de datos     |
| `DB_USER`     | Usuario de PostgreSQL          |
| `DB_PASSWORD` | Contraseña de PostgreSQL       |
| `DB_HOST`     | Host de PostgreSQL             |
| `DB_PORT`     | Puerto de PostgreSQL           |
