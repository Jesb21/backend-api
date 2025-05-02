import bcrypt
from sqlalchemy.orm import Session
from models import User, Place
import schemas
from jose import JWTError, jwt
from datetime import datetime, timedelta
import requests
from typing import TypedDict

# Definir el tipo de `place_data` usando `TypedDict`
class PlaceData(TypedDict):
    name: str
    category: str
    rating: float
    latitude: float
    longitude: float
    address: str

# Clave secreta para JWT
SECRET_KEY = "e55314ila053"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Función para autenticar al usuario
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return False
    return user

# Función para crear un usuario
def create_user(db: Session, user: schemas.UserCreate):
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user.username, password_hash=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener lugares cercanos utilizando la API de Foursquare
def get_nearby_places(lat: float, lon: float, api_key: str):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": api_key}
    params = {
        "ll": f"{lat},{lon}",  # Latitud y longitud
        "radius": 1000,  # Radio de búsqueda en metros (1 km)
        "limit": 10,  # Limitar a 10 resultados
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        places = response.json().get('results', [])

        # Crear un diccionario de datos para cada lugar
        place_data_list = []
        for place in places:
            place_data = PlaceData(
                name=place.get("name"),
                category=place.get("category", {}).get("name", "Unknown"),  # Algunas veces la categoría puede estar vacía
                rating=place.get("rating", 0.0),
                latitude=place.get("location", {}).get("lat", 0.0),
                longitude=place.get("location", {}).get("lng", 0.0),
                address=place.get("location", {}).get("address", "Unknown")
            )

            place_data_list.append(place_data)

        return place_data_list
    else:
        return {"error": "No se pudieron obtener los datos de Foursquare"}

# Función para crear un lugar en la base de datos
def create_place(db: Session, place_data: PlaceData):
    """
    Verifica si el lugar ya existe en la base de datos antes de insertarlo.
    Si el lugar ya existe, lo devuelve; si no, lo crea y lo agrega a la base de datos.
    """
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
