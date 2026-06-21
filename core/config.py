# app/core/config.py
import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
   
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "")
    ALLOWED_CREDENTIALS:bool=os.getenv("ALLOWED_CREDENTIALS","False")

    REDIS_URL:str=os.getenv("REDIS_URL","")
    DATABASE_URL:str=os.getenv("DATABASE_URL","")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()