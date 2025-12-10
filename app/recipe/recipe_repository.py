# app/recipe/recipe_repository.py

from sqlalchemy.orm import Session
from . import recipe_model


def get_recipe(db: Session, recipe_id: int):
    """Busca uma receita específica pelo ID."""
    return (
        db.query(recipe_model.Recipe)
        .filter(recipe_model.Recipe.id == recipe_id)
        .first()
    )


def get_recipes(db: Session):
    """Busca todas as receitas cadastradas."""
    return db.query(recipe_model.Recipe).all()


def get_recipe_by_title(db: Session, title: str):
    """Busca uma receita pelo título (usado para validação de duplicidade)."""
    return (
        db.query(recipe_model.Recipe)
        .filter(recipe_model.Recipe.title == title)
        .first()
    )


def create_recipe(db: Session, recipe: recipe_model.RecipeCreate, user_id: int):
    """
    Cria uma nova receita no banco de dados.
    Agora recebe 'user_id' para vincular a receita ao criador.
    """
    recipe_data = recipe.model_dump()

    db_recipe = recipe_model.Recipe(
        **recipe_data,
        owner_id=user_id
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def update_recipe(db: Session, db_recipe: recipe_model.Recipe, recipe_in):
    """
    Atualiza uma receita existente.
    recipe_in pode ser:
        - RecipeUpdate (Pydantic)
        - dict (enviado pelo service já filtrado)
    """

    # Se vier um Pydantic model
    if hasattr(recipe_in, "model_dump"):
        update_data = recipe_in.model_dump(exclude_unset=True)
    else:
        update_data = dict(recipe_in)

    # Remove campos que o front envia mas não existem no banco
    update_data.pop("category", None)
    update_data.pop("time_minutes", None)
    update_data.pop("image_url", None)

    for key, value in update_data.items():
        setattr(db_recipe, key, value)

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, db_recipe: recipe_model.Recipe):
    """Remove uma receita do banco de dados."""
    db.delete(db_recipe)
    db.commit()
    return db_recipe
