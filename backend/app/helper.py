from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Security
from app.config import settings
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import Token, TokenObj, UserOut
from app.redis_client import redis_client


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


def decode_access_token(token: str) -> TokenObj:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return TokenObj(**payload)


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
    token = decode_access_token(creds.credentials)
    print(f"Decoded token: {token.sub}")  # Debugging output
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ungültiges Token")
    user = db.query(User).filter(User.username == token.sub).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User nicht gefunden")
    return user


async def get_current_user_with_cache(
    creds: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db),
) -> UserOut:
    """
    Prüft das Bearer-Token und lädt den User aus Redis-Cache oder Postgres.
    Cache-First-Strategie für bessere Performance.
    """
    token = decode_access_token(creds.credentials)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ungültiges Token")

    # Versuche zuerst aus Redis-Cache zu laden
    cached_user = redis_client.get_user_cache(token.sub)
    if cached_user:
        print(f"User {token.sub} aus Redis-Cache geladen")
        return cached_user

    # Fallback: Lade aus Postgres und speichere in Cache
    user = db.query(User).filter(User.username == token.sub).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User nicht gefunden")

    # Erstelle UserOut-Objekt und speichere in Cache
    user_out = UserOut(id=user.id, username=user.username, created_at=user.created_at)
    redis_client.set_user_cache(user.username, user_out)
    print(f"User {token.sub} aus Postgres geladen und in Redis gespeichert")

    return user_out
