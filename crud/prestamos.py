from sqlalchemy.orm import Session
import models.prestamo as prestamo_model
import schemas.prestamo as prestamo_schema
from typing import List, Optional

def get_prestamo(db: Session, id_prestamo: int) -> Optional[prestamo_model.Prestamo]:
    """
    Obtiene un préstamo por su ID.
    """
    return db.query(prestamo_model.Prestamo).filter(prestamo_model.Prestamo.id_prestamo == id_prestamo).first()

def get_prestamos(db: Session, skip: int = 0, limit: int = 10) -> List[prestamo_model.Prestamo]:
    """
    Obtiene una lista de préstamos con paginación.
    """
    return db.query(prestamo_model.Prestamo).offset(skip).limit(limit).all()

def create_prestamo(db: Session, prestamo: prestamo_schema.PrestamoCreate) -> prestamo_model.Prestamo:
    """
    Crea un nuevo préstamo en la base de datos.
    """
    db_prestamo = prestamo_model.Prestamo(
        id_usuarios=prestamo.id_usuarios,
        id_material=prestamo.id_material,
        fecha_prestamo=prestamo.fecha_prestamo,
        fecha_devolucion=prestamo.fecha_devolucion,
        estado_prestamo=prestamo.estado_prestamo
    )
    
    db.add(db_prestamo)  # Se pasa el objeto db_prestamo a db.add
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo
