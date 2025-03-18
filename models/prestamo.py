from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from config.db import Base
import enum

class EstadoPrestamo(str, enum.Enum):
    activo = "Activo"
    devuelto = "Devuelto"
    vencido = "Vencido"

class Prestamo(Base):
    __tablename__ = "tbb_prestamo"

    id_prestamo = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey("tbb_users.id"))  # Referencia a usuarios
    id_material = Column(Integer, ForeignKey("tbb_material.id_material"))  # Referencia a materiales
    fecha_prestamo = Column(DateTime)  # Fecha del préstamo
    fecha_devolucion = Column(DateTime, nullable=True)  # Puede ser NULL hasta que se devuelva
    estado_prestamo = Column(Enum(EstadoPrestamo), default=EstadoPrestamo.activo)  # Estado del préstamo
