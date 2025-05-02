from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modelo para la tabla `users`
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    # Relación con la tabla de lugares (para favoritos)
    places = relationship("Place", secondary="user_places", back_populates="users")

# Modelo para la tabla `places`
class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Nombre del lugar
    category = Column(String)  # Categoría del lugar
    rating = Column(Float)  # Puntuación del lugar
    latitude = Column(Float)  # Latitud del lugar
    longitude = Column(Float)  # Longitud del lugar
    address = Column(String)  # Dirección del lugar
    created_at = Column(String)  # Fecha de creación (opcional, usa datetime si prefieres)

    # Relación con la tabla de usuarios (para los favoritos)
    users = relationship("User", secondary="user_places", back_populates="places")

# Tabla intermedia para la relación muchos a muchos entre `users` y `places`
class UserPlace(Base):
    __tablename__ = "user_places"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)  # Relación con `users`
    place_id = Column(Integer, ForeignKey("places.id"), primary_key=True)  # Relación con `places`