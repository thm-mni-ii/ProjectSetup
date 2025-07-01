from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.include_router(router, prefix="/api", tags=["auth"])
