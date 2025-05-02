from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float

# Corregir la URL de la base de datos para Windows Authentication usando DSN configurado
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://SQLServerLocal"

# Crea el engine de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define la clase base para los modelos
Base = declarative_base()

def create_place(db: Session, place_data: dict):
    # Importación diferida para evitar la importación circular
    from models import Place
    
    # Verificar si el lugar ya existe en la base de datos por nombre
    existing_place = db.query(Place).filter(Place.name == place_data["name"]).first()
    if existing_place:
        return existing_place  # Devuelve el lugar existente si ya está en la base de datos
    
    # Si no existe, crear uno nuevo
    new_place = Place(**place_data)
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place
