from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any
from models.models import Couple 
from utils.utils import get_env  


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
    
    from db.sqlite import NewSQLiteClient
    if DB_TYPE == "sqlite":
        return NewSQLiteClient("db/db.sqlite3")
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")
