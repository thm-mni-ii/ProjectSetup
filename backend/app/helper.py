from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Security
from app.config import settings
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(sub: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db),
) -> User:
    """
    Prüft das Bearer-Token und lädt den User aus Postgres.
    Wirft 401, wenn Token fehlt/ungültig oder User nicht existiert.
    """
    username = decode_access_token(creds.credentials)
    if not username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ungültiges Token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User nicht gefunden")
    return user
