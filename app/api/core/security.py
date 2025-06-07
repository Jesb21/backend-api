from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api.database import get_db
from app.api.models.user import User
from app.api.schemas.user import UserInDB
import logging
from passlib.context import CryptContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SECRET_KEY = "eilaeila55314"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def get_user(db: Session, username: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if user:
        logger.debug(f"Usuario encontrado: {user.username}")
    else:
        logger.debug(f"Usuario no encontrado: {username}")
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    logger.debug(f"Intentando autenticar usuario: {username}")
    user = get_user(db, username)
    if not user:
        logger.debug("Usuario no encontrado")
        return None
    if not user.verify_password(password):
        logger.debug("Contraseña incorrecta")
        return None
    logger.debug("Usuario autenticado exitosamente")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Token creado exitosamente")
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token decodificado exitosamente")
        return payload
    except JWTError as e:
        logger.error(f"Error al decodificar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    logger.debug(f"Usuario actual obtenido: {user.username}")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user_from_token)) -> User:
    logger.debug(f"Usuario activo actual obtenido: {current_user.username}")
    return current_user

def get_current_user_from_cookie(request: Request) -> dict:
    token = request.cookies.get("token")
    if not token:
        logger.error("Token no encontrado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            logger.error("Username no encontrado en el token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    except Exception as e:
        logger.error(f"Error al obtener usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def verify_session(request: Request):
    try:
        token = request.cookies.get("token")
        if not token:
            logger.error("Token no encontrado en las cookies")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        get_current_user_from_cookie(request)
        
        return await request.scope["endpoint"](**request.scope["kwargs"])
    except HTTPException as e:
        logger.error(f"Error en verificación de sesión: {str(e)}")
        raise e
