from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    """Esquema base para usuario"""
    username: str
    email: EmailStr
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Esquema para crear un usuario"""
    password: str

class User(UserBase):
    """Esquema completo de usuario"""
    id: int
    created_at: datetime
    updated_at: datetime
    favorite_places: List[int] = []

    class Config:
        """Configuración de Pydantic"""
        from_attributes = True

class UserInDB(User):
    """Esquema para usuario en la base de datos"""
    hashed_password: str

class UserLogin(BaseModel):
    """Esquema para login de usuario"""
    username: str
    password: str
