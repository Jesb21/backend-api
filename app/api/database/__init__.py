from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.api.core.config import get_settings

# Crea el engine de SQLAlchemy
settings = get_settings()
engine = create_engine(
    "sqlite:///database.db",  # Actualizar la URL de la base de datos para usar SQLite
    connect_args={"check_same_thread": False}
)

# Crea una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define la clase base para los modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos
async def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear todas las tablas
async def init_db():
    """Inicializar la base de datos"""
    from app.api.models import User, Place, UserPlace
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada")

# Funciones para manejo de lugares
async def create_place(db: Session, place_data: dict):
    """
    Crear un nuevo lugar o devolver uno existente.
    
    Args:
        db: Sesión de base de datos
        place_data: Datos del lugar
    
    Returns:
        Place: El lugar creado o existente
    """
    from app.api.models.place import Place
    
    # Verificar si el lugar ya existe en la base de datos por nombre
    existing_place = db.query(Place).filter(Place.name == place_data["name"]).first()
    if existing_place:
        return existing_place
    
    # Si no existe, crear uno nuevo
    new_place = Place(**place_data)
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

async def get_places(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lugares"""
    pass

async def get_place_by_id(db: Session, place_id: int):
    """Obtener lugar por ID"""
    pass

# Funciones para manejo de usuarios
async def get_user_by_username(db: Session, username: str):
    """Obtener usuario por username"""
    pass

async def create_user(db: Session, user_data: dict):
    """Crear un nuevo usuario"""
    pass
