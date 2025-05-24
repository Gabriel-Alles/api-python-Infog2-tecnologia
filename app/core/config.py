import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    PROJECT_NAME: str = "RRMARTAN ATELIÊ"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()