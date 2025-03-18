from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud.prestamos import get_prestamos, get_prestamo, create_prestamo
import config.db
import schemas.prestamo as prestamo_schema
import models.prestamo as prestamo_model
from typing import List

prestamo_router = APIRouter()

prestamo_model.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@prestamo_router.get("/prestamos/", response_model=List[prestamo_schema.prestamo], tags=["Préstamos"])
async def read_prestamos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_prestamos(db=db, skip=skip, limit=limit)

# Endpoint para obtener un préstamo por su ID
@prestamo_router.get("/prestamos/{id_prestamos}", response_model=prestamo_schema.prestamo, tags=["Préstamos"])
async def read_prestamo(id_prestamos: int, db: Session = Depends(get_db)):
    db_prestamo = get_prestamo(db=db, prestamo_id=id_prestamos)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return db_prestamo

# Endpoint para crear un nuevo préstamo
@prestamo_router.post("/prestamos/", response_model=prestamo_schema.prestamo, tags=["Préstamos"])
async def create_new_prestamo(prestamo: prestamo_schema.PrestamoCreate, db: Session = Depends(get_db)):
    return create_prestamo(db=db, prestamo=prestamo)

# Endpoint para actualizar un préstamo
@prestamo_router.put("/prestamos/{id_prestamo}", response_model=prestamo_schema.prestamo, tags=["Préstamos"])
async def update_prestamo(id_prestamo: int, prestamo: prestamo_schema.PrestamoUpdate, db: Session = Depends(get_db)):
    db_prestamo = get_prestamo(db=db, id_prestamo=id_prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Actualizar los datos del préstamo
    db_prestamo.fecha_prestamo = prestamo.fecha_prestamo  # Cambié 'fecha_prestamos' por 'fecha_prestamo'
    db_prestamo.fecha_devolucion = prestamo.fecha_devolucion
    db_prestamo.estado_prestamo = prestamo.estado_prestamo
    db_prestamo.id_usuarios = prestamo.id_usuarios
    db_prestamo.id_material = prestamo.id_material

    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo
