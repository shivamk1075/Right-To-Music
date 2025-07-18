

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Union
# from models import Couple  # Make sure models/couple.py has the required definitions
# Debug
from models.models import Couple  # Make sure models/couple.py has the required definitions

# from utils.env import get_env  # You’ll write this based on GetEnv from utils
# Debug
from utils.utils import get_env  # You’ll write this based on GetEnv from utils

# from db.mongo_client import NewMongoClient
# from db.sqlite_client import NewSQLiteClient
# Dg
# from db.mongo import NewMongoClient
# from db.sqlite import NewSQLiteClient



class DBClient(ABC):
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def store_fingerprints(self, fingerprints: Dict[int, Couple]) -> None:
        pass

    @abstractmethod
    def get_couples(self, addresses: List[int]) -> Tuple[Dict[int, List[Couple]], None]:
        pass

    @abstractmethod
    def total_songs(self) -> Tuple[int, None]:
        pass

    @abstractmethod
    def register_song(self, song_title: str, song_artist: str, yt_id: str) -> Tuple[int, None]:
        pass

    @abstractmethod
    def get_song(self, filter_key: str, value: Any) -> Tuple['Song', bool, None]:
        pass

    @abstractmethod
    def get_song_by_id(self, song_id: int) -> Tuple['Song', bool, None]:
        pass

    @abstractmethod
    def get_song_by_ytid(self, yt_id: str) -> Tuple['Song', bool, None]:
        pass

    @abstractmethod
    def get_song_by_key(self, key: str) -> Tuple['Song', bool, None]:
        pass

    @abstractmethod
    def delete_song_by_id(self, song_id: int) -> None:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        pass


class Song:
    def __init__(self, title: str, artist: str, youtube_id: str):
        self.title = title
        self.artist = artist
        self.youtube_id = youtube_id


DB_TYPE = get_env("DB_TYPE", "sqlite")


def new_db_client() -> DBClient:
    # # Dg
    from db.mongo import NewMongoClient
    from db.sqlite import NewSQLiteClient
    if DB_TYPE == "mongo":
        db_username = get_env("DB_USER")
        db_password = get_env("DB_PASS")
        db_name     = get_env("DB_NAME")
        db_host     = get_env("DB_HOST")
        db_port     = get_env("DB_PORT")

        if db_username and db_password:
            db_uri = f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            db_uri = "mongodb://localhost:27017"

        return NewMongoClient(db_uri)

    elif DB_TYPE == "sqlite":
        return NewSQLiteClient("db/db.sqlite3")

    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")
