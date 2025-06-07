# Recomienda App - Backend API

API REST para el sistema de recomendación de lugares cercanos, desarrollada con FastAPI y Python.

## Características

- Autenticación JWT segura
- Búsqueda de lugares cercanos por geolocalización
- Gestión de usuarios (registro, login, perfil)
- Sistema de favoritos para lugares
- Documentación automática con Swagger UI y ReDoc
- Validación de datos con Pydantic
- Base de datos SQLite con SQLAlchemy ORM

## Requisitos

- Python 3.8+
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd backend-api
```

2. Crear y activar entorno virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración

El archivo `.env` debe contener las siguientes variables:

```env
# Configuración de la aplicación
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de base de datos
DATABASE_URL=sqlite:///./database.db
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.api.app:app --reload
```

La aplicación estará disponible en:
- API: http://localhost:8000
- Documentación Swagger UI: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Documentación de la API

La API sigue el estándar REST y está documentada con OpenAPI. Puedes acceder a la documentación interactiva en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints principales

#### Autenticación
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener información del usuario actual

#### Lugares
- `GET /api/places/nearby` - Buscar lugares cercanos
- `GET /api/places/{place_id}` - Obtener detalles de un lugar
- `POST /api/places/` - Crear un nuevo lugar (requiere autenticación)
- `PUT /api/places/{place_id}` - Actualizar un lugar (requiere autenticación)
- `DELETE /api/places/{place_id}` - Eliminar un lugar (requiere autenticación)

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

## Seguridad

- Autenticación JWT
- Hashing de contraseñas con bcrypt
- Validación de datos de entrada
- Manejo de errores personalizado

## Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Créditos

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)
