from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import user_repository, user_model

def create_new_user(db: Session, user: user_model.UserCreate):
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # A lógica de buscar o role foi removida, pois o ID agora vem do controller
    return user_repository.create_user(db=db, user=user, role_id=user.role_id)

def authenticate_user(db: Session, email: str, password: str):
    """Autentica um usuário e retorna os dados se válido."""
    from app.security import verify_password
    
    user = user_repository.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )
    return user

def get_all_users(db: Session):
    return user_repository.get_users(db)

def get_user_by_id(db: Session, user_id: int):
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def update_existing_user(db: Session, user_id: int, user_in: user_model.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    return user_repository.update_user(db=db, db_user=db_user, user_in=user_in)

def delete_user_by_id(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    return user_repository.delete_user(db=db, db_user=db_user)