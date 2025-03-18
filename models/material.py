from sqlalchemy import Column, Integer, String, Enum
from config.db import Base
import enum

class TipoMaterial(str, enum.Enum):
    cañon = "cañon"
    computadora = "computadora"
    extension = "Extension"

class Estado(str, enum.Enum):
    disponible = "Disponible"
    prestado = "Prestado"
    mantenimiento = "En mantenimiento"
    etc = "etc."

class Material(Base):
    __tablename__ = "tbb_material"

    id_material = Column(Integer, primary_key=True, autoincrement=True)
    tipo_material = Column(Enum(TipoMaterial))
    marca = Column(String(60))
    modelo = Column(String(60))
    estado = Column(Enum(Estado))
