from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql+psycopg://user:password@postgres:5432/mydatabase"
    MONGO_URL: str = "mongodb://user:password@mongodb:27017/"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
