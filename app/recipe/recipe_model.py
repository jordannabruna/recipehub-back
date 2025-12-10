from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from enum import Enum as PyEnum

from app.database import Base


class MealType(PyEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    meal_type = Column(Enum(MealType), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="recipes")


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = None
    instructions: str
    meal_type: MealType


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = Field(None, min_length=3)
    description: str | None = None
    instructions: str | None = None
    meal_type: MealType | None = None


class RecipeOut(RecipeBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
