from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud.materials import get_materials, get_material, create_material  # Importación correcta
import config.db
import schemas.material
import models.material 
from typing import List



material_router = APIRouter()

models.material.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener todos los materiales
@material_router.get("/materials/", response_model=List[schemas.material.Material], tags=["Materiales"])
async def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_materials = get_materials(db=db, skip=skip, limit=limit)
    return db_materials

# Endpoint para obtener un material por su ID
@material_router.get("/materials/{material_id}", response_model=schemas.material.Material, tags=["Materiales"])
async def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = get_material(db=db, id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Endpoint para crear un nuevo material
@material_router.post("/materials/", response_model=schemas.material.Material, tags=["Materiales"])
async def create_new_material(material: schemas.material.MaterialCreate, db: Session = Depends(get_db)):
    db_material = create_material(db=db, material=material)
    return db_material

# Endpoint para eliminar un material por su ID
@material_router.delete("/materials/{material_id}", response_model=schemas.material.Material, tags=["Materiales"])
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = get_material(db=db, id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(db_material)
    db.commit()
    return db_material

# Endpoint para actualizar un material
@material_router.put("/materials/{material_id}", response_model=schemas.material.Material, tags=["Materiales"])
async def update_material(material_id: int, material: schemas.material.MaterialCreate, db: Session = Depends(get_db)):
    db_material = get_material(db=db, id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    # Aquí la actualización de los datos
    db_material.tipo_material = material.tipo_material
    db_material.marca = material.marca
    db_material.modelo = material.modelo
    db_material.estado = material.estado

    db.commit()
    db.refresh(db_material)
    return db_material
