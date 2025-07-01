from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


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
    sub: str
    exp: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# # Blog-Post Schemas
# class PostCreate(BaseModel):
#     title: str
#     content: str


# class CommentCreate(BaseModel):
#     text: str


# class Comment(BaseModel):
#     text: str
#     author_id: str
#     author_username: str
#     created_at: datetime


# class Post(BaseModel):
#     id: str
#     title: str
#     content: str
#     author_id: str
#     author_username: str
#     created_at: datetime
#     comments: List[Comment] = []
