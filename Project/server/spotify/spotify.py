

import requests
import re
import json
import time
import math
from typing import List, Tuple

TOKEN_ENDPOINT = "https://open.spotify.com/get_access_token?reason=transport&productType=web-player"
TRACK_INITIAL_PATH = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=getTrack&variables="
PLAYLIST_INITIAL_PATH = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=fetchPlaylist&variables="
ALBUM_INITIAL_PATH = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=getAlbum&variables="
TRACK_END_PATH = '{"persistedQuery":{"version":1,"sha256Hash":"e101aead6d78faa11d75bec5e36385a07b2f1c4a0420932d374d89ee17c70dd6"}}'
PLAYLIST_END_PATH = '{"persistedQuery":{"version":1,"sha256Hash":"b39f62e9b566aa849b1780927de1450f47e02c54abf1e66e513f96e849591e41"}}'
ALBUM_END_PATH = '{"persistedQuery":{"version":1,"sha256Hash":"46ae954ef2d2fe7732b4b2b4022157b2e18b7ea84f70591ceb164e4de1b5d5d3"}}'

class Track:
    def __init__(self, title: str, artist: str, album: str, artists: List[str], duration: int):
        self.title = title
        self.artist = artist
        self.album = album
        self.artists = artists
        self.duration = duration

    def build_track(self):
        return Track(self.title, self.artist, self.album, self.artists, self.duration)

def access_token() -> str:
    response = requests.get(TOKEN_ENDPOINT)
    response.raise_for_status()
    body = response.json()
    return body["accessToken"]

def request(endpoint: str) -> Tuple[int, str]:
    headers = {"Authorization": "Bearer " + access_token()}
    response = requests.get(endpoint, headers=headers)
    return response.status_code, response.text

def get_id(url: str) -> str:
    parts = url.split("/")
    return parts[4].split("?")[0]

def is_valid_pattern(url: str, pattern: str) -> bool:
    return bool(re.match(pattern, url))

def track_info(url: str) -> Track:
    track_pattern = r"^https:\/\/open\.spotify\.com\/track\/[a-zA-Z0-9]{22}\?si=[a-zA-Z0-9]{16}$"
    if not is_valid_pattern(url, track_pattern):
        raise ValueError("invalid track url")

    track_id = get_id(url)
    endpoint_query = json.dumps({"uri": f"spotify:track:{track_id}"})
    endpoint = f"{TRACK_INITIAL_PATH}{endpoint_query}&extensions={PLAYLIST_END_PATH}"

    status_code, json_response = request(endpoint)
    if status_code != 200:
        raise ValueError(f"Received non-200 status code: {status_code}")

    all_artists = []
    first_artist = json.loads(json_response).get("data", {}).get("trackUnion", {}).get("firstArtist", {}).get("items", [])[0].get("profile", {}).get("name")
    if first_artist:
        all_artists.append(first_artist)

    artists = json.loads(json_response).get("data", {}).get("trackUnion", {}).get("otherArtists", {}).get("items", [])
    for artist in artists:
        profile = artist.get("profile", {})
        name = profile.get("name")
        if name:
            all_artists.append(name)

    duration_in_seconds = json.loads(json_response).get("data", {}).get("trackUnion", {}).get("duration", {}).get("totalMilliseconds", 0) // 1000

    track = Track(
        title=json.loads(json_response).get("data", {}).get("trackUnion", {}).get("name"),
        artist=first_artist,
        artists=all_artists,
        duration=duration_in_seconds,
        album=json.loads(json_response).get("data", {}).get("trackUnion", {}).get("albumOfTrack", {}).get("name"),
    )

    return track.build_track()

def playlist_info(url: str) -> List[Track]:
    playlist_pattern = r"^https:\/\/open\.spotify\.com\/playlist\/[a-zA-Z0-9]{22}\?si=[a-zA-Z0-9]{16}$"
    if not is_valid_pattern(url, playlist_pattern):
        raise ValueError("invalid playlist url")

    return resource_info(url, "playlist")

def album_info(url: str) -> List[Track]:
    album_pattern = r"^https:\/\/open\.spotify\.com\/album\/[a-zA-Z0-9-]{22}\?si=[a-zA-Z0-9_-]{22}$"
    if not is_valid_pattern(url, album_pattern):
        raise ValueError("invalid album url")

    return resource_info(url, "album")

def resource_info(url: str, resource_type: str) -> List[Track]:
    resource_id = get_id(url)
    e_conf = {"Limit": 400, "Offset": 0}
    json_response = json_list(resource_type, resource_id, e_conf["Offset"], e_conf["Limit"])

    total_count = json.loads(json_response).get("data", {}).get("playlistV2", {}).get("content", {}).get("totalCount", 0)
    if total_count < 1:
        raise ValueError("hum, there are no tracks")

    requests_count = math.ceil(total_count / e_conf["Limit"])
    tracks = process_items(json_response, resource_type)

    for i in range(1, requests_count):
        e_conf["Offset"] = e_conf["Offset"] + e_conf["Limit"]
        json_response = json_list(resource_type, resource_id, e_conf["Offset"], e_conf["Limit"])
        tracks.extend(process_items(json_response, resource_type))

    return tracks

def json_list(resource_type: str, resource_id: str, offset: int, limit: int) -> str:
    if resource_type == "playlist":
        endpoint_query = json.dumps({"uri": f"spotify:playlist:{resource_id}", "offset": offset, "limit": limit})
        endpoint = f"{PLAYLIST_INITIAL_PATH}{endpoint_query}&extensions={PLAYLIST_END_PATH}"
    else:
        endpoint_query = json.dumps({"uri": f"spotify:album:{resource_id}", "locale": "", "offset": offset, "limit": limit})
        endpoint = f"{ALBUM_INITIAL_PATH}{endpoint_query}&extensions={ALBUM_END_PATH}"

    status_code, json_response = request(endpoint)
    if status_code != 200:
        raise ValueError(f"Received non-200 status code: {status_code}")
    
    return json_response

def process_items(json_response: str, resource_type: str) -> List[Track]:
    item_list = "data.playlistV2.content.items" if resource_type == "playlist" else "data.albumUnion.tracks.items"
    song_title = "itemV2.data.name" if resource_type == "playlist" else "track.name"
    artist_name = "itemV2.data.artists.items.0.profile.name" if resource_type == "playlist" else "track.artists.items.0.profile.name"
    album_name = "itemV2.data.albumOfTrack.name" if resource_type == "playlist" else "data.albumUnion.name"
    duration = "itemV2.data.trackDuration.totalMilliseconds" if resource_type == "playlist" else "track.duration.totalMilliseconds"

    tracks = []
    items = json.loads(json_response).get("data", {}).get("playlistV2", {}).get("content", {}).get("items", [])

    for item in items:
        duration_in_seconds = item.get(duration, 0) // 1000
        track = Track(
            title=item.get(song_title, ""),
            artist=item.get(artist_name, ""),
            album=item.get(album_name, ""),
            artists=[item.get(artist_name, "")],
            duration=duration_in_seconds,
        )
        tracks.append(track.build_track())

    return tracks
