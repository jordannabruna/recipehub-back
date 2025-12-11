import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Importação organizada dos controllers
from app.users import user_controller
from app.roles import role_controller
from app.auth import auth_controller
from app.recipe import recipe_controller

# Lê a variável de ambiente, padrão é "DEV" se não existir
APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

# Cria as tabelas automaticamente em DEV e PROD
Base.metadata.create_all(bind=engine)

# Inicializa as roles padrão
from app.database import SessionLocal
from app.roles.role_model import Role

db = SessionLocal()
try:
    if not db.query(Role).filter_by(name="admin").first():
        admin_role = Role(id=1, name="admin")
        db.add(admin_role)
        db.commit()
    
    if not db.query(Role).filter_by(name="user").first():
        user_role = Role(id=2, name="user")
        db.add(user_role)
        db.commit()
finally:
    db.close()

app = FastAPI(
    title="API do RecipeHub",
    version="0.1.0"
)

# --- CONFIGURAÇÃO DO CORS ---
# Definimos as origens permitidas baseadas no ambiente

if APP_PROFILE == "DEV":
    # Em DEV, listamos as portas comuns usadas localmente pelo Flutter Web e React
    origins = [
        "http://localhost",
        "http://localhost:8080",    # Flutter Web default
        "http://127.0.0.1:8080",    # Flutter Web IP
        "http://localhost:3000",    # React/Next default
        "http://127.0.0.1:3000",
    ]
else:
    # Em PROD (Render), aceita domínios do Render
    origins = [
        "https://recipehub-frontend-ov5q.onrender.com",
        "https://recipehub-front-nm-1.onrender.com",
        "https://recipehub-frontend.onrender.com",
        "https://recipehub-app.onrender.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Importante para enviar Cookies/Headers de Auth
    allow_methods=["*"],    # Libera GET, POST, PUT, DELETE, PATCH, OPTIONS
    allow_headers=["*"],    # Libera todos os headers
)

# --- ROTAS ---
app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)
app.include_router(recipe_controller.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)