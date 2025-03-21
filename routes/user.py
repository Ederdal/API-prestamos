from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud.users import get_users, get_user, create_user, get_user_by_credentials
import config.db
import schemas.user
import models.user
from typing import List
from jwt_config import solicita_token
from portadortoken import Portador
from fastapi.responses import JSONResponse

user = APIRouter()

models.user.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener todos los usuarios (PROTEGIDO)
@user.get(
    "/users/", 
    response_model=List[schemas.user.user], 
    tags=["Usuarios"], 
)
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = get_users(db=db, skip=skip, limit=limit)
    return db_users

# Endpoint para obtener un usuario por su ID (PROTEGIDO)
@user.get(
    "/users/{user_id}", 
    response_model=schemas.user.user, 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]  # Protección con JWT
)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint para crear un nuevo usuario (PROTEGIDO)
@user.post(
    "/users/", 
    response_model=schemas.user.user, 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]  # Protección con JWT
)
async def create_new_user(user: schemas.user.userCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

# Endpoint para eliminar un usuario por su ID (PROTEGIDO)
@user.delete(
    "/users/{user_id}", 
    response_model=schemas.user.user, 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]  # Protección con JWT
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user

# Endpoint para actualizar un usuario por su ID (PROTEGIDO)
@user.put(
    "/users/{user_id}", 
    response_model=schemas.user.user, 
    tags=["Usuarios"], 
    dependencies=[Depends(Portador())]  # Protección con JWT
)
async def update_user(user_id: int, user: schemas.user.userCreate, db: Session = Depends(get_db)):
    db_user = get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualiza los datos del usuario
    db_user.name = user.name
    db_user.lastName = user.lastName
    db_user.typeUser = user.typeUser
    db_user.userName = user.userName
    db_user.email = user.email
    db_user.password = user.password
    db_user.phoneNumber = user.phoneNumber
    db_user.status = user.status
    db_user.registrationDate = user.registrationDate
    db_user.updateDate = user.updateDate or None

    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint de login (SIN PROTECCIÓN, para obtener el token)

@user.post("/login", tags=["User Login"])
def read_credentials(ususario: schemas.user.UserLogin, db: Session = Depends(get_db)):
    db_credentials = get_user_by_credentials(
        db,
        userName=ususario.userName,
        password=ususario.password,
    )
    if db_credentials is None:
        return JSONResponse(content={'mensaje': 'Acceso denegado'}, status_code=404)

    # Se genera el token y se retorna en la respuesta
    token: str = solicita_token(ususario.dict())
    return JSONResponse(status_code=200, content={"token": token})
