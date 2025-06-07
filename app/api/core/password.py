from argon2 import PasswordHasher
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pwd_hasher = PasswordHasher()

class PasswordManager:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            logger.debug(f"Verificando contraseña para hash: {hashed_password[:10]}...")
            result = pwd_hasher.verify(hashed_password, plain_password)
            logger.debug(f"Resultado de verificación: {result}")
            return result
        except Exception as e:
            logger.error(f"Error al verificar contraseña: {str(e)}")
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        try:
            hash = pwd_hasher.hash(password)
            logger.debug(f"Contraseña hasheada exitosamente")
            return hash
        except Exception as e:
            logger.error(f"Error al hashear contraseña: {str(e)}")
            raise Exception("Error al procesar la contraseña")

password_manager = PasswordManager()
