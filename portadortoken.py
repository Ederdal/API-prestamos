from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jwt_config import valida_token
import crud.users, config.db, models.user

models.user.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Portador(HTTPBearer):
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        autorizacion: HTTPAuthorizationCredentials = await super().__call__(request)
        if not autorizacion or not autorizacion.credentials:
            raise HTTPException(status_code=403, detail="Token no proporcionado")

        try:
            dato = valida_token(autorizacion.credentials)
        except Exception:
            raise HTTPException(status_code=403, detail="Token inválido o corrupto")

        userName = dato.get("userName")
        password = dato.get("password")

        if not userName or not password:
            raise HTTPException(status_code=403, detail="Token inválido: faltan credenciales")

        db_userlogin = crud.users.get_user_by_credentials(
            db=db,
            userName=userName,
            password=password
        )

        if db_userlogin is None:
            raise HTTPException(status_code=403, detail="Token inválido o usuario no encontrado")

        return db_userlogin
