from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = 'lazyfox'
    POSTGRES_PASSWORD: str = 'lazyfox@123'
    POSTGRES_DB: str = 'your_dbname'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()