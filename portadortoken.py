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
        # Obtiene las credenciales del token
        autorizacion: HTTPAuthorizationCredentials = await super().__call__(request)
        dato = valida_token(autorizacion.credentials)

        # Verifica las credenciales en la base de datos
        db_userlogin = crud.users.get_user_by_credentials(
            db,
            userName=dato["userName"],  # Ajusta estos campos según tu modelo
            email=dato["email"],
            phoneNumber=dato["phoneNumber"],
            password=dato["password"]
        )

        if db_userlogin is None:
            raise HTTPException(status_code=403, detail="Token inválido o usuario no encontrado")

        # Retorna los datos del usuario autenticado
        return db_userlogin
