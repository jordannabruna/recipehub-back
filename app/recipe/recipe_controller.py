from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from . import recipe_service, recipe_model
from app.auth.auth_service import get_current_user
from app.users.user_model import User


router = APIRouter(prefix="/recipes", tags=["Recipes"])


def recipe_to_public(recipe: recipe_model.Recipe):
    return {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description or "",
        "instructions": recipe.instructions or "",
        "category": getattr(recipe, "category", "General") or "General",
        "time_minutes": getattr(recipe, "time_minutes", 0) or 0,
        "image_url": getattr(recipe, "image_url", "") or "",
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: recipe_model.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_recipe = recipe_service.create_new_recipe(
        db=db,
        recipe=recipe,
        user_id=current_user.id
    )
    return recipe_to_public(new_recipe)


@router.get("/")
def read_recipes(db: Session = Depends(get_db)):
    recipes = recipe_service.get_all_recipes(db)
    return [recipe_to_public(r) for r in recipes]


@router.get("/{recipe_id}")
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipe_service.get_recipe_by_id(db, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe_to_public(recipe)


@router.put("/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe: recipe_model.RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = recipe_service.update_existing_recipe(
        db=db,
        recipe_id=recipe_id,
        recipe_in=recipe
    )

    return recipe_to_public(updated)


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = recipe_service.delete_recipe_by_id(db=db, recipe_id=recipe_id)
    return recipe_to_public(deleted)
