
import os
import random
import time


def generate_unique_id() -> int:
    random.seed(time.time())
    return random.randint(0, 2**32 - 1)


def generate_song_key(song_title: str, song_artist: str) -> str:
    return f"{song_title}---{song_artist}"


def get_env(key: str, fallback: str = "") -> str:
    return os.getenv(key, fallback)
