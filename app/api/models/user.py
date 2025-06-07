from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.api.database import Base
from datetime import datetime
from app.api.core.password import password_manager

class User(Base):
    """Modelo para usuarios"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con lugares favoritos
    user_places = relationship("UserPlace", back_populates="user")

    def set_password(self, password: str):
        """Establece la contraseña hasheada"""
        self.hashed_password = password_manager.get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        return password_manager.verify_password(password, self.hashed_password)
