import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.database import engine, Base
from app.users import user_controller
from app.roles import role_controller
from app.auth import auth_controller

APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

if APP_PROFILE == "DEV":
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

if APP_PROFILE == "DEV":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://recipehub-front-nm-1.onrender.com",
            "https://recipehub-front-nm-1.onrender.com/",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)

from app.recipe import recipe_controller
app.include_router(recipe_controller.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)