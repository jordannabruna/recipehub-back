from sqlalchemy.orm import Session
from . import user_model
from app.security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_users(db: Session):
    return db.query(user_model.User).all()


def create_user(db: Session, user: user_model.UserCreate, role_id: int):
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.name,
        profile_image_url=user.profile_image_url,
        role_id=role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: user_model.User, user_in: user_model.UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
         if key == "password":
             setattr(db_user, "hashed_password", get_password_hash(value))
         else:
             setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: user_model.User):
    role = db_user.role
    db.delete(db_user)
    db.commit()
    db_user.role = role
    return db_user