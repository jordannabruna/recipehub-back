from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from app.database import Base
from app.roles.role_model import RolePublic


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True, nullable=True)
    profile_image_url = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: Annotated[str, Field(min_length=3)]
    profile_image_url: str | None = None
    role_id: int | None = Field(default=1, description="ID do role a ser associado ao usuário")
    
    model_config = ConfigDict(populate_by_name=True)

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None = None
    profile_image_url: str | None = None
    role: RolePublic

class UserLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None = None
    profile_image_url: str | None = None
    role: RolePublic
    token: str