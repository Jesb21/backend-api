# Inicialización de las rutas de la API
from fastapi import APIRouter

from .auth import auth_router
from .places import places_router

# Crear un router principal con el prefijo /api/v1
api_router = APIRouter(prefix="/api/v1")

# Incluir las rutas de autenticación y lugares
api_router.include_router(auth_router)
api_router.include_router(places_router)

# Exportar el router principal
__all__ = ["api_router"]
