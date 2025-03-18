from sqlalchemy import Column, Integer, String, DateTime, Enum
from config.db import Base
import enum

class TypeUser(str, enum.Enum):
    Student = "Student"
    Teacher = "Teacher"
    Secretary = "Secretary"
    Laboratory = "Laboratory"
    Executive = "Executive"
    Administrative = "Administrative"

class Status(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Blocked = "Blocked"
    Suspended = "Suspended"

class User(Base):
    __tablename__ = "tbb_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    lastName = Column(String(60))
    typeUser = Column(Enum(TypeUser))
    userName = Column(String(60))
    email = Column(String(100))
    password = Column(String(60))
    phoneNumber = Column(String(20))
    status = Column(Enum(Status))
    registrationDate = Column(DateTime)
    updateDate = Column(DateTime)