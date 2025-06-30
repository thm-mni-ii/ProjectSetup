from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserOut, Token
from app.models import User
from app.helper import hash_password, verify_password, create_access_token
from app.helper import get_db, get_current_user, get_current_user_with_cache
from app.config import settings
from app.redis_client import redis_client

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=user.username, password_hash=hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserOut(id=user.id, username=user.username, created_at=user.created_at)


@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    """
    Login a user and return an access token.
    """
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ungültige Anmeldedaten")

    # Bei erfolgreichem Login: Cache user data in Redis
    user_out = UserOut(id=user.id, username=user.username, created_at=user.created_at)
    redis_client.set_user_cache(user.username, user_out)

    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(user: UserOut = Depends(get_current_user_with_cache)):
    """
    Geschützter Endpoint – liefert den aktuell eingeloggten User.
    Verwendet Redis-Cache für bessere Performance bei hohem Traffic.
    """
    return user