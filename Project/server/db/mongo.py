

from pymongo import MongoClient as PyMongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from typing import Dict, List, Tuple, Any
# from models.couple import Couple
# Dg
from models.models import Couple

from db.client import DBClient, Song

# from utils.env import get_env
# Dg
from utils.utils import get_env

# from utils.helpers import generate_unique_id, generate_song_key  # You must define these
# Dg
from utils.utils import generate_unique_id, generate_song_key  # You must define these

class MongoClient(DBClient):
    def __init__(self, uri: str):
        self.client = PyMongoClient(uri)
        self.db = self.client["song-recognition"]

    def close(self):
        if self.client:
            self.client.close()

    def store_fingerprints(self, fingerprints: Dict[int, Couple]) -> None:
        collection = self.db["fingerprints"]
        for address, couple in fingerprints.items():
            filter_doc = {"_id": address}
            update_doc = {
                "$push": {
                    "couples": {
                        "anchorTimeMs": couple.anchor_time_ms,
                        "songID": couple.song_id
                    }
                }
            }
            collection.update_one(filter_doc, update_doc, upsert=True)

    def get_couples(self, addresses: List[int]) -> Tuple[Dict[int, List[Couple]], None]:
        collection = self.db["fingerprints"]
        couples_map = {}

        for address in addresses:
            result = collection.find_one({"_id": address})
            if not result:
                continue

            couples = []
            for item in result.get("couples", []):
                couples.append(Couple(
                    anchor_time_ms=int(item["anchorTimeMs"]),
                    song_id=int(item["songID"])
                ))
            couples_map[address] = couples

        return couples_map, None

    def total_songs(self) -> Tuple[int, None]:
        total = self.db["songs"].count_documents({})
        return total, None

    def register_song(self, song_title: str, song_artist: str, yt_id: str) -> Tuple[int, None]:
        collection = self.db["songs"]
        collection.create_index([("ytID", ASCENDING), ("key", ASCENDING)], unique=True)

        song_id = generate_unique_id()
        key = generate_song_key(song_title, song_artist)
        doc = {"_id": song_id, "key": key, "ytID": yt_id}

        try:
            collection.insert_one(doc)
        except DuplicateKeyError:
            raise Exception("Song with ytID or key already exists.")
        except Exception as e:
            raise Exception(f"Failed to register song: {e}")

        return song_id, None

    def get_song(self, filter_key: str, value: Any) -> Tuple[Song, bool, None]:
        if filter_key not in ["_id", "ytID", "key"]:
            raise ValueError("Invalid filter key")

        song = self.db["songs"].find_one({filter_key: value})
        if not song:
            return Song("", "", ""), False, None

        key_parts = song["key"].split("---")
        return Song(
            title=key_parts[0],
            artist=key_parts[1],
            youtube_id=song["ytID"]
        ), True, None

    def get_song_by_id(self, song_id: int) -> Tuple[Song, bool, None]:
        return self.get_song("_id", song_id)

    def get_song_by_ytid(self, yt_id: str) -> Tuple[Song, bool, None]:
        return self.get_song("ytID", yt_id)

    def get_song_by_key(self, key: str) -> Tuple[Song, bool, None]:
        return self.get_song("key", key)

    def delete_song_by_id(self, song_id: int) -> None:
        self.db["songs"].delete_one({"_id": song_id})

    def delete_collection(self, collection_name: str) -> None:
        self.db[collection_name].drop()


def NewMongoClient(uri: str) -> MongoClient:
    return MongoClient(uri)
