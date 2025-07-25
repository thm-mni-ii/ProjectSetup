from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql+psycopg://user:password@postgres:5432/mydatabase"
    POSTGRES_URL_PSYCOPG: str = "postgresql://user:password@postgres:5432/mydatabase"
    MONGO_URL: str = "mongodb://user:password@mongodb:27017/"
    REDIS_URL: str = "redis://:password@redis:6379/0"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_CACHE_EXPIRE_MINUTES: int = 60  # Cache-Ablaufzeit in Minuten


settings = Settings()
