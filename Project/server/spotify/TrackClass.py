from typing import List

class Track:
    def __init__(self, title: str, artist: str, album: str, artists: List[str], duration: int):
        self.title = title
        self.artist = artist
        self.album = album
        self.artists = artists
        self.duration = duration

    def build_track(self):
        return Track(self.title, self.artist, self.album, self.artists, self.duration)
