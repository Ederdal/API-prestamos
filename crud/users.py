import models.user
import schemas.user
from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, id: int):
    return db.query(models.user.User).filter(models.user.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.user.User).offset(skip).limit(limit).all()

def get_user_by_credentials(db:Session, userName: str, email: str, phoneNumber: str, password: str):
    return db.query(models.user.User).filter((models.user.User.userName == userName) | (models.user.User.email == email) | (models.user.User.phoneNumber == phoneNumber), models.user.User.password == password).first()



def create_user(db: Session, user: schemas.user.userCreate):
    db_user = models.user.User(
        name=user.name,  
        lastName=user.lastName,  
        typeUser=user.typeUser,
        userName=user.userName,
        email=user.email,
        password=user.password,
        phoneNumber=user.phoneNumber, 
        status=user.status,
        registrationDate=user.registrationDate,
        updateDate=user.updateDate or None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
