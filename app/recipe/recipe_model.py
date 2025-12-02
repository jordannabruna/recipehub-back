# app/recipe/recipe_model.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel, Field, ConfigDict

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Relacionamento com Usuário
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Importante: Como sua pasta chama "users" (plural), o caminho deve ser esse:
    owner = relationship("app.users.user_model.User") 

# ==================================
# SCHEMAS (Pydantic)
# ==================================

# Usado para criar uma nova receita (campos obrigatórios)
class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    instructions: str | None = None

# Usado para atualizar (tudo opcional) - ESTAVA FALTANDO ESTE AQUI
class RecipeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    instructions: str | None = None

# Usado para retornar dados ao front-end
class RecipePublic(BaseModel):
    id: int
    title: str
    description: str | None = None
    instructions: str | None = None
    owner_id: int

    # Configuração atualizada para Pydantic V2 (remove o warning)
    model_config = ConfigDict(from_attributes=True)