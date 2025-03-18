import models.material
import schemas.material
from sqlalchemy.orm import Session
import models, schemas

def get_material(db: Session, id: int):
    return db.query(models.material.Material).filter(models.material.Material.id_material == id).first()

def get_materials(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.material.Material).offset(skip).limit(limit).all()

def create_material(db: Session, material: schemas.material.MaterialCreate):
    db_material = models.material.Material(
        tipo_material=material.tipo_material,
        marca=material.marca,
        modelo=material.modelo,
        estado=material.estado
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
