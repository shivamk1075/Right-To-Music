

import os
import time
import shutil
import logging
import threading
import concurrent.futures
import subprocess

from pathlib import Path
from typing import List, Tuple

# from server.spotify.track_info import TrackInfo, PlaylistInfo, AlbumInfo, GetYoutubeId
# from server.spotify.models import Track
# from server.utils.logger import get_logger
# from server.utils.file_ops import delete_file, get_file_size
# from server.wav import wav_utils
# from server.shazam import spectro_utils
# from server.db.client import DBClient
# from server.spotify.metadata import YtIDExists, SongKeyExists

# IMPORTED EVERYTHING assuming always just the main.py is ran from the server inside directory
# new imports statements after debugging
from .spotify import track_info, playlist_info, album_info
from .youtube import get_youtube_id
from .spotify import Track
from utils.logger import get_logger
from utils.helpers import delete_file
from .utils import get_file_size
# from wav.wav import wav_utils 
# New debugged import
import wav.wav as wav
import wav.convert as convert

# from shazam.shazam import spectro_utils
# New debug
from shazam.spectrogram import Spectrogram, ExtractPeaks
from shazam.fingerprint import Fingerprint
# from db.client import DBClient
# Above was creating issue : abstract class methods
from db.client import new_db_client

from .utils import yt_id_exists, song_key_exists
import params

logger = get_logger()
DELETE_SONG_FILE = False

def dl_single_track(url: str, save_path: str) -> Tuple[int, Exception]:
    # track_info = TrackInfo(url)
    # track_info = track_info(url)
    TrackInfo = track_info(url)
    if not TrackInfo:
        # return 0, Exception("TrackInfo fetch failed")
        return 0, Exception("track_info fetch failed")
    print("Getting track info...")
    time.sleep(0.5)
    print("Now, downloading track...")
    # return dl_track([track_info], save_path)
    # Dg
    return dl_track([TrackInfo], save_path)

def dl_playlist(url: str, save_path: str) -> Tuple[int, Exception]:
    # tracks = PlaylistInfo(url)
    tracks = playlist_info(url)
    if not tracks:
        # return 0, Exception("PlaylistInfo fetch failed")
        return 0, Exception("playlist_info fetch failed")
    time.sleep(1)
    print("Now, downloading playlist...")
    return dl_track(tracks, save_path)

def dl_album(url: str, save_path: str) -> Tuple[int, Exception]:
    # tracks = AlbumInfo(url)
    tracks = album_info(url)
    if not tracks:
        # return 0, Exception("AlbumInfo fetch failed")
        return 0, Exception("album_info fetch failed")
    time.sleep(1)
    print("Now, downloading album...")
    return dl_track(tracks, save_path)

def dl_track(tracks: List[Track], path: str) -> Tuple[int, Exception]:
    total_downloaded = 0
    os.makedirs(path, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_track, track, path) for track in tracks]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                total_downloaded += 1
    print("Total tracks downloaded:", total_downloaded)
    return total_downloaded, None

def process_track(track: Track, path: str) -> bool:
    track_key = f"{track.title} - {track.artist}"
    # if SongKeyExists(track_key):
    if song_key_exists(track_key):
        logger.info(f"{track_key} already exists.")
        return False

    yt_id = get_yt_id(track)
    if not yt_id:
        logger.error(f"Failed to get YouTube ID for {track_key}")
        return False

    file_name = f"{track.title} - {track.artist}"
    file_path = os.path.join(path, file_name + ".m4a")
    if not download_yt_audio(yt_id, file_path):
        return False

    if not process_and_save_song(file_path, track.title, track.artist, yt_id):
        return False

    delete_file(file_path)
    wav_file = os.path.join(path, file_name + ".wav")
    if not add_tags(wav_file, track):
        return False

    if DELETE_SONG_FILE:
        delete_file(wav_file)
    print(f"'{track.title}' by '{track.artist}' was downloaded")
    return True

# def download_yt_audio(yt_id: str, output_path: str) -> bool:
#     from pytube import YouTube
#     try:
#         yt = YouTube(f"https://youtube.com/watch?v={yt_id}")
#         stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
#         if not stream:
#             return False
#         stream.download(filename=output_path)
#         return get_file_size(output_path) > 0
#     except Exception as e:
#         logger.error(f"Download failed: {e}")
#         return False
# def download_yt_audio(yt_id: str, output_path: str) -> bool:
#     url = f"https://youtube.com/watch?v={yt_id}"
#     cmd = [
#         "yt-dlp",
#         "-f", "bestaudio[ext=m4a]/bestaudio/best",
#         "-o", output_path,
#         url
#     ]
#     try:
#         subprocess.run(cmd, check=True)
#         return os.path.exists(output_path) and os.path.getsize(output_path) > 0
#     except Exception as e:
#         print(f"yt-dlp download failed: {e}")
#         return False
def download_yt_audio(yt_id: str, output_path: str) -> bool:
    url = f"https://youtube.com/watch?v={yt_id}"
    base, _ = os.path.splitext(output_path)
    cmd = [
        "yt-dlp",
        "-f", "bestaudio[ext=m4a]/bestaudio/best",
        "-o", base + ".%(ext)s",
        url
    ]
    try:
        subprocess.run(cmd, check=True)
        # Find the actual file (could be .m4a or .webm)
        for ext in ("m4a", "webm", "mp3", "opus"):
            candidate = base + f".{ext}"
            if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
                if candidate != output_path:
                    os.rename(candidate, output_path)
                return True
        return False
    except Exception as e:
        print(f"yt-dlp download failed: {e}")
        return False

def add_tags(file_path: str, track: Track) -> bool:
    temp_file = file_path.replace(".wav", "2.wav")
    cmd = [
        "ffmpeg", "-i", file_path, "-c", "copy",
        "-metadata", f"album_artist={track.artist}",
        "-metadata", f"title={track.title}",
        "-metadata", f"artist={track.artist}",
        "-metadata", f"album={track.album}",
        temp_file
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        shutil.move(temp_file, file_path)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Tagging failed: {e}")
        return False

def process_and_save_song(wav_path: str, title: str, artist: str, yt_id: str) -> bool:
    # db = DBClient()
    # Dg
    db = new_db_client()


    # wav_path = wav_utils.convert_to_wav(file_path)
    # wav_info = wav_utils.read_wav_info(wav_path)
    # samples = wav_utils.bytes_to_samples(wav_info.data)
    # New debug
    # wav_path = convert.convert_to_wav(file_path)
    # Dg
    #Dg
    # wav_path = convert.convert_to_wav(file_path,1)

    # #Dg
    # # Using unsed reformat func here 
    # wav_path=convert.reformat_wav(wav_path,1)
    
    wav_info = wav.read_wav_info(wav_path)
    # samples = wav.wav_bytes_to_samples(wav_info.data)
    # New dg
    samples = wav.wav_bytes_to_samples(wav_info['data'])

    # spectro = spectro_utils.compute_spectrogram(samples, wav_info.sample_rate)
    # Debug
    # spectro = Spectrogram(samples, wav_info.sample_rate)
    # Dg
    spectro = Spectrogram(samples, wav_info['sample_rate'])


    # song_id = db.register_song(title, artist, yt_id)
    # Dg
    try:
        song_id = db.register_song(title, artist, yt_id)
    except ValueError as e:
        print(f"[INFO] {e}")
        return None  # or return an existing song ID from a lookup

    # peaks = spectro_utils.extract_peaks(spectro, wav_info.duration)
    # fingerprints = spectro_utils.fingerprint(peaks, song_id)
    # New debug
    # peaks = ExtractPeaks(spectro, wav_info.duration)
    # Dg
    peaks = ExtractPeaks(spectro, wav_info['duration'])
    fingerprints = Fingerprint(peaks, song_id)
    if not db.store_fingerprints(fingerprints):
        db.delete_song_by_id(song_id)
        return False
    print(f"Fingerprint for {title} by {artist} saved in DB successfully")
    return True

# def get_yt_id(track: Track) -> str:
#     yt_id = GetYoutubeId(track)
#     if not yt_id or YtIDExists(yt_id):
#         yt_id = GetYoutubeId(track)
#         if not yt_id or YtIDExists(yt_id):
#             return ""
#     return yt_id
# new debugged one
def get_yt_id(track: Track) -> str:
    yt_id = get_youtube_id(track)
    if not yt_id or yt_id_exists(yt_id):
        yt_id = get_youtube_id(track)
        if not yt_id or yt_id_exists(yt_id):
            return ""
    return yt_id
