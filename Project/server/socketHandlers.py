
import base64
import json
import time
import logging

from flask_socketio import SocketIO


from utils.helpers import create_folder
from utils.logger import get_logger
from utils.utils import generate_song_key

import db.client as DBClient

from models.models import RecordData

from shazam.shazam import FindMatchesFGP
from spotify.spotify import album_info, track_info
from spotify.downloader import dl_album, dl_playlist, dl_single_track

from wav.wav import write_wav_file

def download_status(status_type, message):
    try:
        data = {"type": status_type, "message": message}
        json_data = json.dumps(data)
        return json_data
    except Exception as e:
        logger = get_logger()
        ctx = {}
        logger.error("Failed to marshal data.", exc_info=e)
        return ""

def handle_total_songs(socket):
    logger = get_logger()
    ctx = {}

    db_client = DBClient.new_db_client()
    try:
        total_songs = db_client.total_songs()
        socket.emit("totalSongs", total_songs)
    except Exception as e:
        logger.error("Error connecting to DB", exc_info=e)

def handle_song_download(socket, spotify_url):
    logger = get_logger()
    ctx = {}

    try:
        if "album" in spotify_url:
            tracks_in_album = album_info(spotify_url)
            status_msg = f"{len(tracks_in_album)} songs found in album."
            socket.emit("downloadStatus", download_status("info", status_msg))

            total_tracks_downloaded = dl_album(spotify_url, "SONGS_DIR")
            status_msg = f"{total_tracks_downloaded} songs downloaded from album"
            socket.emit("downloadStatus", download_status("success", status_msg))

        elif "playlist" in spotify_url:
            tracks_in_playlist = album_info(spotify_url) 
            status_msg = f"{len(tracks_in_playlist)} songs found in playlist."
            socket.emit("downloadStatus", download_status("info", status_msg))

            total_tracks_downloaded = dl_playlist(spotify_url, "SONGS_DIR")
            status_msg = f"{total_tracks_downloaded} songs downloaded from playlist."
            socket.emit("downloadStatus", download_status("success", status_msg))

        elif "track" in spotify_url:
            track_info_data = track_info(spotify_url)
            db_client = DBClient.new_db_client()
            song, song_exists = db_client.get_song_by_key(generate_song_key(track_info_data['title'], track_info_data['artist']))

            if song_exists:
                status_msg = f"'{song['title']}' by '{song['artist']}' already exists in the database (https://www.youtube.com/watch?v={song['youtube_id']})"
                socket.emit("downloadStatus", download_status("error", status_msg))
                return

            total_downloads = dl_single_track(spotify_url, "SONGS_DIR")
            if total_downloads != 1:
                status_msg = f"'{track_info_data['title']}' by '{track_info_data['artist']}' failed to download"
                socket.emit("downloadStatus", download_status("error", status_msg))
            else:
                status_msg = f"'{track_info_data['title']}' by '{track_info_data['artist']}' was downloaded"
                socket.emit("downloadStatus", download_status("success", status_msg))
    except Exception as e:
        logger.error("Error handling song download", exc_info=e)

def handle_new_recording(socket, record_data):
    logger = get_logger()
    ctx = {}

    try:
        rec_data = json.loads(record_data)
        rec_data = RecordData(**rec_data)

        create_folder("recordings")
        now = time.localtime()
        file_name = f"{now.tm_sec}_{now.tm_min}_{now.tm_hour}_{now.tm_mday}_{now.tm_mon}_{now.tm_year}.wav"
        file_path = f"recordings/{file_name}"

        decoded_audio_data = base64.b64decode(rec_data.audio)

        write_wav_file(file_path, decoded_audio_data, rec_data.sampleRate, rec_data.channels, rec_data.sampleSize)
    except Exception as e:
        logger.error("Failed to handle new recording", exc_info=e)



def handle_new_fingerprint(socket, fingerprint_data):
    logger = get_logger()
    ctx = {}

    try:
        data = json.loads(fingerprint_data)
        fingerprint = data.get('fingerprint', {})

        matches, _, err = FindMatchesFGP(fingerprint)
        if err:
            logger.error("Failed to get matches", exc_info=err)
            return

    
        json_data = json.dumps([match.__dict__ for match in (matches[:10] if len(matches) > 10 else matches)])
        socket.emit("matches", json_data)
    except Exception as e:
        logger.error("Failed to handle new fingerprint", exc_info=e)
