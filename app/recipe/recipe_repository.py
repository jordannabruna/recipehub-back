from sqlalchemy.orm import Session
from . import recipe_model

def get_recipe(db: Session, recipe_id: int):
    return db.query(recipe_model.Recipe).filter(recipe_model.Recipe.id == recipe_id).first()

def get_recipes(db: Session):
    return db.query(recipe_model.Recipe).all()

def create_recipe(db: Session, recipe: recipe_model.RecipeCreate):
    db_recipe = recipe_model.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update_recipe(db: Session, db_recipe: recipe_model.Recipe, recipe_in: recipe_model.RecipeUpdate):
    update_data = recipe_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recipe, key, value)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, db_recipe: recipe_model.Recipe):
    db.delete(db_recipe)
    db.commit()
    return db_recipe

def get_recipe_by_title(db: Session, title: str):
    return db.query(recipe_model.Recipe).filter(recipe_model.Recipe.title == title).first()
