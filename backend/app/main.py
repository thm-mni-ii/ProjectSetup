from fastapi import Depends, FastAPI
from app.database import engine
from app.database import Base
from app.routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secondhand Marktplatz API")

app.include_router(router, prefix="/api", tags=["auth"])
