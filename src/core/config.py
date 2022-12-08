# Will contain Pydantic Base settings for having the Config from .env file
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_secret_key:str
    refresh_token_expire_minutes:int

    class Config:
        env_file = ".env"
 

settings = Settings()