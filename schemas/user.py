from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import datetime

class userBase(BaseModel):
    name: str
    lastName: str
    typeUser: str
    userName: str
    email: str
    password: str
    phoneNumber: str
    status: str
    registrationDate: datetime
    updateDate: datetime

class userCreate(userBase):
    pass
class userUpdate(userBase):
    pass
class user(userBase):
    id: int
    class config:
        orm_mode = True
        
class UserLogin(BaseModel):
    userName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    password: str