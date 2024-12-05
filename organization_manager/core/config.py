from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./organization_manager.db"
    SECRET_KEY = "193d659e-8499-4562-a348-772e3be98e0c"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
