"""
Controlador de Roles (Perfis)
"""
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal
from app.roles.role_model import Role
from app.users.user_model import User
from app.security import get_password_hash
import pytest
import random
import string

# FIXTURES DE CONFIGURAÇÃO

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Garante tabelas criadas."""
    Base.metadata.create_all(bind=engine)
    yield

def get_auth_headers(client, email, password, role_name):
    """
    Função auxiliar para criar um usuário com uma Role específica,
    fazer login e retornar os headers com o Token.
    """
    db = SessionLocal()
    
    # Garante a Role
    role = db.query(Role).filter_by(name=role_name).first()
    if not role:
        role = Role(name=role_name, description=f"Role {role_name} criada pelo teste")
        db.add(role)
        db.commit()
        db.refresh(role)

    # Garante o Usuário
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name=f"User {role_name}",
            role_id=role.id
        )
        db.add(user)
        db.commit()
    db.close()

    # Faz Login
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def admin_headers():
    """Retorna headers de autenticação de um ADMINISTRADOR."""
    client = TestClient(app)
    return get_auth_headers(client, "admin_test@recipehub.com", "admin123", "admin")

@pytest.fixture(scope="module")
def user_headers():
    """Retorna headers de autenticação de um USUÁRIO COMUM."""
    client = TestClient(app)
    return get_auth_headers(client, "common_user@recipehub.com", "user123", "user")

# TESTES DE SUCESSO (ADMIN)

def test_create_role_as_admin(admin_headers):
    """Admin deve conseguir criar uma nova role."""
    client = TestClient(app)
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
    role_name = f"editor_{random_suffix}"
    
    payload = {
        "name": role_name,
        "description": "Pode editar receitas"
    }
    
    response = client.post("/roles/", json=payload, headers=admin_headers)
    assert response.status_code == 201
    data = response.json()
    
    # Validações básicas
    assert data["name"] == role_name
    assert "id" in data
    if "description" in data:
        assert data["description"] == "Pode editar receitas"

def test_list_roles_as_admin(admin_headers):
    """Admin deve conseguir listar todas as roles."""
    client = TestClient(app)
    
    response = client.get("/roles/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 

# TESTES DE SEGURANÇA (USUÁRIO COMUM)

def test_create_role_forbidden_for_user(user_headers):
    """Usuário comum NÃO deve conseguir criar role (Erro 403)."""
    client = TestClient(app)
    
    payload = {"name": "hacker_role", "description": "Tentativa de invasão"}
    
    response = client.post("/roles/", json=payload, headers=user_headers)
    assert response.status_code == 403

def test_list_roles_forbidden_for_user(user_headers):
    """Usuário comum NÃO deve conseguir listar roles (Erro 403)."""
    client = TestClient(app)
    
    response = client.get("/roles/", headers=user_headers)
    assert response.status_code == 403

def test_create_duplicate_role(admin_headers):
    """
    Tentar criar uma role que já existe deve falhar.
    """
    client = TestClient(app)
    
    # Cria uma role
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
    role_name = f"unique_{random_suffix}"
    payload = {"name": role_name, "description": "Original"}
    
    client.post("/roles/", json=payload, headers=admin_headers)
    
    # Tenta criar a mesma role novamente
    response = client.post("/roles/", json=payload, headers=admin_headers)
    
    assert response.status_code != 201