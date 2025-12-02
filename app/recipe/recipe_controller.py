# app/recipe/recipe_controller.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List

from app.database import get_db
from . import recipe_service, recipe_model

# Imports de Segurança (observe o "users" no plural agora)
from app.auth.auth_service import get_current_user
from app.users.user_model import User 

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/", response_model=recipe_model.RecipePublic, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: recipe_model.RecipeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Exige login
):
    """Cria nova receita vinculada ao usuário logado."""
    return recipe_service.create_new_recipe(db=db, recipe=recipe, user_id=current_user.id)

@router.get("/", response_model=List[recipe_model.RecipePublic])
def read_recipes(db: Session = Depends(get_db)):
    """Lista todas as receitas (Público)."""
    return recipe_service.get_all_recipes(db)

@router.get("/{recipe_id}", response_model=recipe_model.RecipePublic)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Busca receita por ID (Público)."""
    return recipe_service.get_recipe_by_id(db, recipe_id=recipe_id)

@router.put("/{recipe_id}", response_model=recipe_model.RecipePublic)
def update_recipe(
    recipe_id: int, 
    recipe: recipe_model.RecipeUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Exige login
):
    """Atualiza receita (Requer Login)."""
    return recipe_service.update_existing_recipe(db=db, recipe_id=recipe_id, recipe_in=recipe)

@router.delete("/{recipe_id}", response_model=recipe_model.RecipePublic)
def delete_recipe(
    recipe_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Exige login
):
    """Deleta receita (Requer Login)."""
    return recipe_service.delete_recipe_by_id(db=db, recipe_id=recipe_id)