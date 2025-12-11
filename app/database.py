from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

connect_args = {}

if APP_PROFILE == "DEV":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./recipehub.db"
    connect_args = {"check_same_thread": False}
else:
    DB_USER = os.getenv('POSTGRES_USER', 'postgresql')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', '12345678')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    DB_NAME = os.getenv('POSTGRES_DB', 'recipe_hub')

    if not DB_PORT or DB_PORT.strip() == '':
        DB_PORT = '5432'

    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()