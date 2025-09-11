# app/user/controller.py
from fastapi import APIRouter, HTTPException, status

from app.user.user_model import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

# Simulação de um banco de dados em memória
fake_db = {
    1: {"id": 1, "email": "user1@example.com", "full_name": "User One", "password": "password1"},
    2: {"id": 2, "email": "user2@example.com", "full_name": "User Two", "password": "password2"},
}

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_id = max(fake_db.keys() or [0]) + 1
    new_user_data = user.model_dump()
    new_user_data["id"] = new_id
    fake_db[new_id] = new_user_data
    return UserPublic(**new_user_data)

@router.get("/", response_model=list[UserPublic])
def list_users():
    # Converte os dicionários do 'banco de dados' para o modelo público
    return [UserPublic(**user_data) for user_data in fake_db.values()]

@router.put("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stored_user_data = fake_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True) # Apenas campos enviados

    updated_user = stored_user_data.copy()
    updated_user.update(update_data)
    fake_db[user_id] = updated_user

    return UserPublic(**updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    del fake_db[user_id]
    # Com status 204, a resposta não deve ter corpo. O FastAPI cuida disso.
