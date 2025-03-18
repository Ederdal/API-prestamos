from jwt import encode, decode, ExpiredSignatureError
from datetime import datetime, timedelta

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

def solicita_token(dato: dict) -> str:
    expiracion = datetime.utcnow() + timedelta(hours=1)  # El token expira en 1 hora
    dato["exp"] = expiracion  # Se añade la expiración al payload
    token = encode(payload=dato, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def valida_token(token: str) -> dict:
    try:
        dato = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return dato
    except ExpiredSignatureError:
        raise Exception("El token ha expirado")
    except Exception as e:
        raise Exception(f"Token inválido: {str(e)}")
