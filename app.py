from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from crud import create_user, authenticate_user, create_access_token, get_nearby_places
from schemas import UserCreate, UserLogin
from database import SessionLocal, engine
from models import Base
import os
from dotenv import load_dotenv
from jose import JWTError, jwt

# Cargar las variables de entorno desde el archivo .env
load_dotenv()  # Esto carga automáticamente el archivo .env

# Definir las variables de configuración para JWT
SECRET_KEY = "e55314ila053"  # Usa una clave secreta segura en un entorno real
ALGORITHM = "HS256"  # Algoritmo de firma para el JWT

# Instancia de la aplicación FastAPI
app = FastAPI()

# Configuración de CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes temporalmente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia para obtener el token de autorización (si se usa JWT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Ruta para el registro de usuarios
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return {"message": "Usuario creado con éxito", "user": db_user.username}

# Ruta para el login de usuarios
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db=db, username=user.username, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Crear el token JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para obtener lugares cercanos usando Foursquare
@app.get("/places")
def get_places(lat: float, lon: float, db: Session = Depends(get_db)):
    api_key = os.getenv("FOURSQUARE_API_KEY")  # Usa una variable de entorno para la API Key
    if not api_key:
        raise HTTPException(status_code=500, detail="Foursquare API Key no configurada")
    
    places = get_nearby_places(lat, lon, api_key)
    
    if "error" in places:
        raise HTTPException(status_code=500, detail="Error al obtener lugares de Foursquare")
    
    return {"places": places}

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para verificar el token JWT (si usas JWT para autenticación)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="No se pudo validar las credenciales", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
