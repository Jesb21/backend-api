from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.database import get_db
from app.api.models.user import User as UserModel
from app.api.schemas.user import UserCreate, User, UserLogin
from app.api.core.security import authenticate_user, create_access_token
import logging
from fastapi.responses import JSONResponse

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=User)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    logger.debug(f"Intentando registrar usuario: {user_in.username}")
    # Verificar si el usuario ya existe
    db_user = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if db_user:
        logger.debug("Usuario ya existe")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if db_user:
        logger.debug("Email ya existe")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Crear nuevo usuario
    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        is_active=True
    )
    
    # Hashear la contraseña
    db_user.set_password(user_in.password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.debug(f"Usuario registrado exitosamente: {db_user.username}")
    return db_user

@auth_router.post("/login", response_model=User)
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    logger.debug(f"Intentando login con usuario: {user_in.username}")
    user = authenticate_user(db, user_in.username, user_in.password)
    
    if not user:
        logger.debug("Credenciales inválidas")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    logger.debug("Credenciales válidas")
    
    # Crear token de acceso
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    
    # Crear respuesta con cookie
    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email
            }
        }
    )
    
    # Establecer cookie con el token
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,  # En producción debería ser True
        max_age=30 * 60,  # 30 minutos
        path="/"
    )
    
    logger.debug("Token generado y cookie establecida")
    return response
