from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from pydantic import BaseModel, Field

# Modelo SQLAlchemy
class Recipe(Base):
	__tablename__ = "recipes"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(100), nullable=False, index=True)
	description = Column(Text, nullable=True)
	instructions = Column(Text, nullable=True)

# Schemas Pydantic
class RecipeCreate(BaseModel):
	title: str = Field(..., min_length=3, max_length=100)
	description: str | None = None
	instructions: str | None = None

class RecipeUpdate(BaseModel):
	title: str | None = Field(default=None, min_length=3, max_length=100)
	description: str | None = None
	instructions: str | None = None

class RecipePublic(BaseModel):
	id: int
	title: str
	description: str | None = None
	instructions: str | None = None

	class Config:
		orm_mode = True
