from typing import List, Union, Optional
from pydantic import BaseModel

class materialBase(BaseModel):
    tipo_material: str
    marca: str
    modelo: str
    estado: str

class MaterialCreate(materialBase):
    pass
class MaterialUpdate(materialBase):
    pass
class Material(materialBase):
    id_material: int
    class Config:
        orm_mode = True