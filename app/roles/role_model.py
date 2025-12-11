from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict
from app.database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class RoleCreate(BaseModel):
    name: str


class RolePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str