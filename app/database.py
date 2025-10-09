from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

APP_PROFILE =   os.getenv("APP_PROFILE", "DEV")

if APP_PROFILE == "DEV":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./recipehub.db"
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("APP_PROFILE")

DB_USER = os.getenv('POSTGRES_USER', 'postgresql')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', '12345678')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'recipe_hub')

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SQLALCHEMY_DATABASE_URL = "sqlite:///./recipehub.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
