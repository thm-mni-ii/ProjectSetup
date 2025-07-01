from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
import redis

from app.config import settings

# Postgres
engine = create_engine(settings.POSTGRES_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# MongoDB
mongo_client = MongoClient(settings.MONGO_URL)
mongo_db = mongo_client["blog"]

# Redis
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
