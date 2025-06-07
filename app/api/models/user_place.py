from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.api.database import Base

class UserPlace(Base):
    __tablename__ = "user_places"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    is_favorite = Column(Boolean, default=True)

    user = relationship("User", back_populates="user_places")
    place = relationship("Place", back_populates="user_places")
