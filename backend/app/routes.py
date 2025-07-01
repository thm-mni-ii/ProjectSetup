from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from bson import ObjectId

# from app.schemas import UserCreate, UserOut, Token, PostCreate, Post, CommentCreate
from app.models import User
from app.helper import hash_password, verify_password, create_access_token
from app.helper import get_db, get_current_user, get_current_user_with_cache
from app.helper import execute_raw_query
from app.config import settings
from app.redis_client import redis_client
from app.database import mongo_db

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return {"status": "ok", "message": "Service is running"}


# @router.post("/register", response_model=UserOut, status_code=201)
# async def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     """
#     Register a new user.
#     """
#     if db.query(User).filter_by(username=user.username).first():
#         raise HTTPException(status_code=400, detail="Username already exists")

#     user = User(username=user.username, password_hash=hash_password(user.password))
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return UserOut(id=user.id, username=user.username, created_at=user.created_at)


# @router.post("/login", response_model=Token)
# def login(data: UserCreate, db: Session = Depends(get_db)):
#     """
#     Login a user and return an access token.
#     """
#     user = db.query(User).filter_by(username=data.username).first()
#     if not user or not verify_password(data.password, user.password_hash):
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Ungültige Anmeldedaten")

#     # Bei erfolgreichem Login: Cache user data in Redis
#     user_out = UserOut(id=user.id, username=user.username, created_at=user.created_at)
#     redis_client.set_user_cache(user.username, user_out)

#     token = create_access_token(user.username)
#     return {"access_token": token, "token_type": "bearer"}


# @router.get("/me", response_model=UserOut)
# def me(user: User = Depends(get_current_user)):
#     """Geschützter Endpoint – liefert den aktuell eingeloggten User."""

#     return UserOut(id=user.id, username=user.username, created_at=user.created_at)


# @router.get("/me", response_model=UserOut)
# def me(user: UserOut = Depends(get_current_user_with_cache)):
#     """
#     Geschützter Endpoint – liefert den aktuell eingeloggten User.
#     Verwendet Redis-Cache für bessere Performance bei hohem Traffic.
#     """
#     return user


# # MongoDB Collections
# posts_collection = mongo_db["posts"]

# @router.post("/posts", response_model=Post, status_code=201)
# async def create_post(
#     post_data: PostCreate, current_user: UserOut = Depends(get_current_user)
# ):
#     """
#     Erstellt einen neuen Blog-Post in MongoDB.
#     Zeigt wie MongoDB's schemafreie Struktur genutzt wird.
#     """
#     try:
#         # Erstelle Post-Dokument
#         post_doc = {
#             "title": post_data.title,
#             "content": post_data.content,
#             "author_id": str(current_user.id),
#             "author_username": current_user.username,
#             "created_at": datetime.utcnow(),
#             "comments": [],  # Array für Kommentare
#         }

#         # Speichere in MongoDB
#         result = posts_collection.insert_one(post_doc)
#         post_doc["_id"] = str(result.inserted_id)

#         # Konvertiere MongoDB-Dokument zu Pydantic Model
#         return Post(
#             id=post_doc["_id"],
#             title=post_doc["title"],
#             content=post_doc["content"],
#             author_id=post_doc["author_id"],
#             author_username=post_doc["author_username"],
#             created_at=post_doc["created_at"],
#             comments=post_doc["comments"],
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Fehler beim Erstellen des Posts: {str(e)}"
#         )


# @router.get("/posts", response_model=List[Post])
# async def get_posts(skip: int = 0, limit: int = 10):
#     """
#     Holt alle Blog-Posts aus MongoDB.
#     Demonstriert Pagination in MongoDB.
#     """
#     try:
#         # Holt Posts mit Pagination und sortiert nach Erstellungsdatum
#         posts_docs = list(
#             posts_collection.find().skip(skip).limit(limit).sort("created_at", -1)
#         )

#         posts = []
#         for doc in posts_docs:
#             posts.append(
#                 Post(
#                     id=str(doc["_id"]),
#                     title=doc["title"],
#                     content=doc["content"],
#                     author_id=doc["author_id"],
#                     author_username=doc["author_username"],
#                     created_at=doc["created_at"],
#                     comments=[
#                         {
#                             "text": comment["text"],
#                             "author_id": comment["author_id"],
#                             "author_username": comment["author_username"],
#                             "created_at": comment["created_at"],
#                         }
#                         for comment in doc.get("comments", [])
#                     ],
#                 )
#             )

#         return posts

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Fehler beim Laden der Posts: {str(e)}"
#         )


# @router.get("/posts/{post_id}", response_model=Post)
# async def get_post(post_id: str):
#     """
#     Holt einen spezifischen Post anhand der MongoDB ObjectId.
#     """
#     try:
#         post_doc = posts_collection.find_one({"_id": ObjectId(post_id)})

#         if not post_doc:
#             raise HTTPException(status_code=404, detail="Post nicht gefunden")

#         return Post(
#             id=str(post_doc["_id"]),
#             title=post_doc["title"],
#             content=post_doc["content"],
#             author_id=post_doc["author_id"],
#             author_username=post_doc["author_username"],
#             created_at=post_doc["created_at"],
#             comments=[
#                 {
#                     "text": comment["text"],
#                     "author_id": comment["author_id"],
#                     "author_username": comment["author_username"],
#                     "created_at": comment["created_at"],
#                 }
#                 for comment in post_doc.get("comments", [])
#             ],
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Fehler beim Laden des Posts: {str(e)}"
#         )


# @router.post("/posts/{post_id}/comments", status_code=201)
# async def add_comment(
#     post_id: str,
#     comment_data: CommentCreate,
#     current_user: UserOut = Depends(get_current_user),
# ):
#     """
#     Fügt einen Kommentar zu einem Post hinzu.
#     Demonstriert MongoDB's Fähigkeit, verschachtelte Dokumente zu speichern.
#     """
#     # Prüfe ob Post existiert
#     try:
#         if not posts_collection.find_one({"_id": ObjectId(post_id)}):
#             raise HTTPException(status_code=404, detail="Post nicht gefunden")
#     except:
#         raise HTTPException(status_code=400, detail="Ungültige Post-ID")

#     # Erstelle Kommentar
#     comment = {
#         "text": comment_data.text,
#         "author_id": str(current_user.id),
#         "author_username": current_user.username,
#         "created_at": datetime.utcnow(),
#     }

#     # Füge Kommentar hinzu
#     try:
#         result = posts_collection.update_one(
#             {"_id": ObjectId(post_id)}, {"$push": {"comments": comment}}
#         )

#         if result.modified_count == 0:
#             raise HTTPException(
#                 status_code=500, detail="Fehler beim Hinzufügen des Kommentars"
#             )

#         return {"message": "Kommentar erfolgreich hinzugefügt"}

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Fehler beim Hinzufügen des Kommentars: {str(e)}"
#         )


# @router.get("/users/{user_id}/posts", response_model=List[Post])
# async def get_user_posts(user_id: str):
#     """
#     Holt alle Posts eines bestimmten Users.
#     Zeigt wie man in MongoDB nach bestimmten Feldern filtert.
#     """
#     posts_docs = list(
#         posts_collection.find({"author_id": user_id}).sort("created_at", -1)
#     )

#     posts = []
#     for doc in posts_docs:
#         posts.append(
#             Post(
#                 id=str(doc["_id"]),
#                 title=doc["title"],
#                 content=doc["content"],
#                 author_id=doc["author_id"],
#                 author_username=doc["author_username"],
#                 created_at=doc["created_at"],
#                 comments=[
#                     {
#                         "text": comment["text"],
#                         "author_id": comment["author_id"],
#                         "author_username": comment["author_username"],
#                         "created_at": comment["created_at"],
#                     }
#                     for comment in doc.get("comments", [])
#                 ],
#             )
#         )

#     return posts


# @router.get("/stats/users-by-month")
# async def get_users_by_month():
#     """
#     Nutzerstatistiken - User Registrierungen pro Monat (letzten 12 Monate)
#     Verwendet raw SQL mit psycopg (ohne ORM)
#     """
#     try:
#         query = """
#         SELECT
#             TO_CHAR(DATE_TRUNC('month', created_at), 'YYYY-MM') as month,
#             COUNT(*) as user_count
#         FROM users
#         WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
#         GROUP BY DATE_TRUNC('month', created_at)
#         ORDER BY DATE_TRUNC('month', created_at) DESC
#         """

#         results = execute_raw_query(query)
#         stats = [{"month": row[0], "user_count": int(row[1])} for row in results]

#         return {"title": "Nutzerregistrierungen pro Monat", "data": stats}
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Fehler beim Laden der Nutzerstatistiken: {str(e)}"
#         )
