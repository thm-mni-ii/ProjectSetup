import redis
import json
from typing import Optional
from app.config import settings
from app.schemas import UserOut


class RedisClient:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def set_user_cache(
        self, username: str, user_data: UserOut, expire_time: Optional[int] = None
    ):
        """
        Speichert Benutzerdaten im Redis-Cache

        Args:
            username: Der Benutzername als Cache-Key
            user_data: Die Benutzerdaten als UserOut-Objekt
            expire_time: Ablaufzeit in Sekunden (Standard: aus Config)
        """
        try:
            if expire_time is None:
                expire_time = settings.REDIS_CACHE_EXPIRE_MINUTES * 60

            cache_key = f"user:{username}"
            user_json = user_data.json()
            self.redis_client.setex(cache_key, expire_time, user_json)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern in Redis: {e}")
            return False

    def get_user_cache(self, username: str) -> Optional[UserOut]:
        """
        Lädt Benutzerdaten aus dem Redis-Cache
        """
        try:
            cache_key = f"user:{username}"
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                user_dict = json.loads(cached_data)
                return UserOut(**user_dict)
            return None
        except Exception as e:
            print(f"Fehler beim Laden aus Redis: {e}")
            return None

    def delete_user_cache(self, username: str) -> bool:
        """
        Löscht Benutzerdaten aus dem Redis-Cache
        """
        try:
            cache_key = f"user:{username}"
            return bool(self.redis_client.delete(cache_key))
        except Exception as e:
            print(f"Fehler beim Löschen aus Redis: {e}")
            return False


# Globale Redis-Instanz
redis_client = RedisClient()
