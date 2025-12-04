from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal
from app.roles.role_model import Role
from app.users.user_model import User
from app.security import get_password_hash
import pytest

# Credenciais para o usuário de teste
LOGIN_EMAIL = "auth_test@recipehub.com"
LOGIN_PASSWORD = "password123"

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Garante tabelas limpas para o teste."""
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="module")
def client_with_user():
    """
    Cria um usuário no banco para testar o login
    """
    client = TestClient(app)
    db = SessionLocal()

    # Garante Role
    role = db.query(Role).filter_by(name="user").first()
    if not role:
        role = Role(name="user")
        db.add(role)
        db.commit()
        db.refresh(role)

    # Garante Usuário
    user = db.query(User).filter_by(email=LOGIN_EMAIL).first()
    if not user:
        user = User(
            email=LOGIN_EMAIL,
            hashed_password=get_password_hash(LOGIN_PASSWORD),
            full_name="Auth Test User",
            role_id=role.id
        )
        db.add(user)
        db.commit()
    
    db.close()
    return client

def test_login_sucesso(client_with_user):
    """
    Testa login com credenciais válidas.
    Deve retornar 200 e um token Bearer.
    """
    response = client_with_user.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    assert response.status_code == 200, f"Login falhou: {response.text}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_senha_invalida(client_with_user):
    """
    Testa login com senha errada.
    Deve retornar 401 Unauthorized.
    """
    response = client_with_user.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": "senhaerrada"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_usuario_inexistente(client_with_user):
    """
    Testa login com email não cadastrado.
    Deve retornar 401 Unauthorized.
    """
    response = client_with_user.post("/auth/login", data={
        "username": "fantasma@recipehub.com",
        "password": "123"
    })
    assert response.status_code == 401