"""
Testes Unitários - Controlador de Usuários

Este arquivo valida o fluxo CRUD completo.
A fixture 'client_and_token' garante que o usuário de login
exista no banco de dados antes de iniciar os testes.
"""

from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal
from app.users.user_model import User
from app.roles.role_model import Role
from app.security import get_password_hash
import pytest
import random
import string

LOGIN_EMAIL = "auth_test@recipehub.com"
LOGIN_PASSWORD = "password123"

@pytest.fixture(scope="module")
def client_and_token():
    """
    1. Conecta no banco.
    2. Cria a Role e o Usuário se não existirem.
    3. Faz o login e retorna o token.
    """
    # Prepara o Banco de Dados 
    db = SessionLocal()
    
    # Garante que existe uma Role
    role = db.query(Role).filter_by(name="admin").first()
    if not role:
        role = Role(name="admin", description="Role criada pelo teste")
        db.add(role)
        db.commit()
        db.refresh(role)
    
    # Garante que o usuário de login existe
    user = db.query(User).filter_by(email=LOGIN_EMAIL).first()
    if not user:
        user = User(
            email=LOGIN_EMAIL,
            hashed_password=get_password_hash(LOGIN_PASSWORD),
            full_name="Usuario Teste Login",
            role_id=role.id
        )
        db.add(user)
        db.commit()
    
    db.close() # Fecha conexão direta com o banco

    # Fazer Login via API
    client = TestClient(app)
    
    login_response = client.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    
    assert login_response.status_code == 200, f"Login falhou: {login_response.text}"
    token = login_response.json()["access_token"]
    
    return client, token

def test_user_crud_sequence(client_and_token):
    """
    Fluxo principal: Cria, Edita e Remove um usuário novo.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # Precisa de uma Role para criar o NOVO usuário
    roles_resp = client.get("/roles/", headers=headers)
    assert roles_resp.status_code == 200, "Erro ao buscar roles"
    roles_list = roles_resp.json()
    assert len(roles_list) > 0, "Nenhuma role disponível"
    role_id = roles_list[0]["id"]

    # Gerar e-mail único
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"novo_user_{random_suffix}@teste.com"

    # 2. CREATE (POST)
    user_data = {
        "email": test_email,
        "password": "senhaNova123",
        "full_name": "User Criado no Teste",
        "role_id": role_id
    }
    create_resp = client.post("/users/", json=user_data, headers=headers)
    assert create_resp.status_code == 201, f"Erro create: {create_resp.text}"
    user_created = create_resp.json()
    user_id = user_created["id"]

    # Valida Create
    assert user_created["email"] == test_email
    # Validação segura da Role (funciona se vier objeto ou ID)
    if "role" in user_created and user_created["role"]:
        assert user_created["role"]["id"] == role_id
    elif "role_id" in user_created:
        assert user_created["role_id"] == role_id

    # UPDATE (PUT)
    update_data = {
        "full_name": "User Atualizado"
    }
    update_resp = client.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200, f"Erro update: {update_resp.text}"
    assert update_resp.json()["full_name"] == "User Atualizado"

    # DELETE (DELETE)
    del_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert del_resp.status_code == 200, f"Erro delete: {del_resp.text}"

    # VERIFICAÇÃO (GET deve dar 404)
    check_resp = client.get(f"/users/{user_id}", headers=headers)
    assert check_resp.status_code == 404