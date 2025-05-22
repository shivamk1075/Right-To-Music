
import sqlite3
from typing import Dict, List, Tuple, Union
from models.models import Couple
from .genClient import Song
import utils.utils as utils

class SQLiteClient:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    ytID TEXT,
                    key TEXT NOT NULL UNIQUE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS fingerprints (
                    address INTEGER NOT NULL,
                    anchorTimeMs INTEGER NOT NULL,
                    songID INTEGER NOT NULL,
                    PRIMARY KEY (address, anchorTimeMs, songID)
                )
            """)

    def close(self):
        self.conn.close()

    def store_fingerprints(self, fingerprints: Dict[int, Couple]):
        with self.conn:
            for address, couple in fingerprints.items():
                try:
                    self.conn.execute(
                        "INSERT OR REPLACE INTO fingerprints (address, anchorTimeMs, songID) VALUES (?, ?, ?)",
                        (int(address), int(couple.anchor_time_ms), int(couple.song_id))
                    )
                except Exception as e:
                    print(f"[ERROR] Failed to insert fingerprint: {e}")
                    print(f"Types => address: {type(address)}, time: {type(couple.anchor_time_ms)}, song_id: {type(couple.song_id)}")
                    return False  
        return True


    def get_couples(self, addresses: List[int]) -> Dict[int, List[Couple]]:
        result = {}
        for address in addresses:
            cursor = self.conn.execute(
                "SELECT anchorTimeMs, songID FROM fingerprints WHERE address = ?",
                (address,)
            )
            rows = cursor.fetchall()
            couples = [Couple(song_id=row[1],anchor_time_ms=row[0]) for row in rows]
            result[address] = couples
        return result

    def total_songs(self) -> int:
        cursor = self.conn.execute("SELECT COUNT(*) FROM songs")
        return cursor.fetchone()[0]

    def register_song(self, title: str, artist: str, yt_id: str) -> int:
        song_id = utils.generate_unique_id()
        song_key = utils.generate_song_key(title, artist)
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO songs (id, title, artist, ytID, key) VALUES (?, ?, ?, ?, ?)",
                    (song_id, title, artist, yt_id, song_key)
                )
            return song_id
        except sqlite3.IntegrityError:
            raise ValueError("Song with this key or ytID already exists.")

    def _get_song(self, filter_key: str, value: Union[int, str]) -> Tuple[Song, bool]:
        if filter_key not in ["id", "ytID", "key"]:
            raise ValueError("Invalid filter key")

        query = f"SELECT title, artist, ytID FROM songs WHERE {filter_key} = ?"
        cursor = self.conn.execute(query, (value,))
        row = cursor.fetchone()
        if row:
            # return Song(title=row[0], artist=row[1], yt_id=row[2]), True
            # Dg
            return Song(title=row[0], artist=row[1], youtube_id=row[2]), True
        return Song("", "", ""), False

    def get_song_by_id(self, song_id: int) -> Tuple[Song, bool]:
        return self._get_song("id", song_id)

    def get_song_by_ytid(self, yt_id: str) -> Tuple[Song, bool]:
        return self._get_song("ytID", yt_id)

    def get_song_by_key(self, key: str) -> Tuple[Song, bool]:
        return self._get_song("key", key)

    def delete_song_by_id(self, song_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM fingerprints WHERE SongID = ?", (song_id,))
            self.conn.execute("DELETE FROM songs WHERE id = ?", (song_id,))

    def delete_collection(self, collection_name: str):
        with self.conn:
            self.conn.execute(f"DROP TABLE IF EXISTS {collection_name}")
def NewSQLiteClient(db_path: str) -> SQLiteClient:
    return SQLiteClient(db_path)