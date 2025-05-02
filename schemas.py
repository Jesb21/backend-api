from pydantic import BaseModel
from typing import Optional

# Esquema base para usuario
class UserBase(BaseModel):
    username: str

# Esquema para crear un usuario
class UserCreate(UserBase):
    password: str  # La contraseña que se proporcionará al crear el usuario

# Esquema para login de usuario
class UserLogin(UserBase):
    password: str  # La contraseña que se proporcionará al iniciar sesión

# Esquema para usuario en la base de datos (incluye la contraseña encriptada)
class UserInDB(UserBase):
    id: int
    password_hash: str  # La contraseña encriptada almacenada en la base de datos

    class Config:
        orm_mode = True
