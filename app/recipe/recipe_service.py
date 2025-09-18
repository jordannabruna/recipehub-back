from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import recipe_repository, recipe_model

def create_new_recipe(db: Session, recipe: recipe_model.RecipeCreate):
    # Regra de negócio: não permitir receitas com o mesmo título
    db_recipe = recipe_repository.get_recipe_by_title(db, title=recipe.title)
    if db_recipe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recipe with this title already exists")
    return recipe_repository.create_recipe(db=db, recipe=recipe)

def get_all_recipes(db: Session):
    return recipe_repository.get_recipes(db)

def get_recipe_by_id(db: Session, recipe_id: int):
    db_recipe = recipe_repository.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return db_recipe

def update_existing_recipe(db: Session, recipe_id: int, recipe_in: recipe_model.RecipeUpdate):
    db_recipe = get_recipe_by_id(db, recipe_id)
    return recipe_repository.update_recipe(db=db, db_recipe=db_recipe, recipe_in=recipe_in)

def delete_recipe_by_id(db: Session, recipe_id: int):
    db_recipe = get_recipe_by_id(db, recipe_id)
    return recipe_repository.delete_recipe(db=db, db_recipe=db_recipe)
