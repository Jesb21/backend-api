from pydantic import BaseModel
from typing import Optional, List

class PlaceBase(BaseModel):
    """Esquema base para lugar"""
    name: str
    category: Optional[str] = None
    rating: Optional[float] = None
    latitude: float
    longitude: float
    address: Optional[str] = None

class PlaceCreate(PlaceBase):
    """Esquema para crear un lugar"""
    pass

class Place(PlaceBase):
    """Esquema completo de lugar"""
    id: int
    created_at: str

    class Config:
        """Configuración de Pydantic"""
        orm_mode = True
