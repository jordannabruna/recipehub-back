# main.py
import uvicorn
from fastapi import FastAPI
from app.user import user_controller
from app.roles import role_controller
from app.auth import auth_controller
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API do Meu Projeto", version="0.1.0")

app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)