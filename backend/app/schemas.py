from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenObj(BaseModel):
    sub: str  # Subject, typically the username
    exp: datetime  # Expiration time of the token

    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM models
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Custom encoder for datetime
        }
