from typing import List, Union, Optional
from pydantic import BaseModel
from datetime   import datetime  

class prestamoBase(BaseModel):
    
   id_usuarios: int
   id_material: int
   fecha_prestamo: datetime  
   fecha_devolucion: datetime  
   estado_prestamo: str

class PrestamoCreate(prestamoBase):
    pass

class PrestamoUpdate(prestamoBase):
    pass

class prestamo(prestamoBase):
    id_prestamo: int
    class Config:  # Corrección en la indentación
        orm_mode = True
