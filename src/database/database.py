from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from pydantic import PostgresDsn



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:\
{settings.database_password}@{settings.database_hostname}:\
{settings.database_port}/{settings.database_name}"

print(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_url():
    return SQLALCHEMY_DATABASE_URL
    