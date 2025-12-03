from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal
from app.roles.role_model import Role
from app.users.user_model import User
from app.security import get_password_hash
import pytest
import random
import string

# Credenciais para o usuário de teste
LOGIN_EMAIL = "teste_pytest@teste.com"
LOGIN_PASSWORD = "senha123456"

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Garante que as tabelas existam antes de rodar os testes.
    """
    Base.metadata.create_all(bind=engine)
    yield
    # Opcional: Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client_and_token():
    """
    1. Cria um usuário de teste no banco (se não existir).
    2. Faz login com esse usuário.
    3. Retorna o cliente e o token para os testes usarem.
    """
    client = TestClient(app)
    db = SessionLocal()

    # --- SEED DE DADOS PARA O TESTE ---
    # 1. Garante que existe uma Role
    role = db.query(Role).filter_by(name="user").first()
    if not role:
        role = Role(name="user")
        db.add(role)
        db.commit()
        db.refresh(role)

    # 2. Garante que existe o Usuário
    user = db.query(User).filter_by(email=LOGIN_EMAIL).first()
    if not user:
        user = User(
            email=LOGIN_EMAIL,
            hashed_password=get_password_hash(LOGIN_PASSWORD),
            full_name="Pytest User",
            role_id=role.id
        )
        db.add(user)
        db.commit()
    
    db.close()
    # ----------------------------------

    # Realiza login via API
    login_response = client.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    
    assert login_response.status_code == 200, f"Erro no Login: {login_response.text}"
    token = login_response.json()["access_token"]
    return client, token

def test_recipe_crud_sequence(client_and_token):
    """
    Testa o fluxo completo: Criar -> Ler -> Atualizar -> Deletar
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # Gera título único para evitar conflito
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    recipe_title = f"Bolo de Teste {random_suffix}"

    # 1. CREATE
    recipe_data = {
        "title": recipe_title,
        "description": "Descrição original",
        "instructions": "Misture tudo."
    }
    create_resp = client.post("/recipes/", json=recipe_data, headers=headers)
    assert create_resp.status_code == 201
    recipe_id = create_resp.json()["id"]
    assert create_resp.json()["owner_id"] is not None

    # 2. READ
    get_resp = client.get(f"/recipes/{recipe_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == recipe_title

    # 3. UPDATE
    update_data = {"description": "Descrição Editada"}
    update_resp = client.put(f"/recipes/{recipe_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["description"] == "Descrição Editada"

    # 4. DELETE
    delete_resp = client.delete(f"/recipes/{recipe_id}", headers=headers)
    assert delete_resp.status_code == 200

    # Confirma que sumiu
    check_resp = client.get(f"/recipes/{recipe_id}", headers=headers)
    assert check_resp.status_code == 404

def test_create_recipe_validations(client_and_token):
    """
    Testa validações: campos obrigatórios e duplicidade.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # Teste 1: Sem Título (Erro 422)
    resp_missing = client.post("/recipes/", json={"description": "Sem título"}, headers=headers)
    assert resp_missing.status_code == 422

    # Teste 2: Título Duplicado (Erro 400)
    unique_title = f"Receita Duplicada {random.randint(1, 9999)}"
    # Cria a primeira
    client.post("/recipes/", json={"title": unique_title}, headers=headers)
    # Tenta a segunda
    resp_dup = client.post("/recipes/", json={"title": unique_title}, headers=headers)
    assert resp_dup.status_code == 400
    assert "already exists" in resp_dup.json()["detail"]