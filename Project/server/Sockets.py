# This file is handles all the socket events for the server.

import base64
import json
import time
import logging
from flask_socketio import SocketIO
from utils.helpers import create_folder
from utils.loggs import get_logger
from utils.utils import generate_song_key
import db.genClient as DBClient
from models.models import RecordData
from shazam.MainShazam import FindMatchesFGP
from wav.wavFuncs import write_wav_file

def handle_total_songs(socket):
    logger = get_logger()
    ctx = {}

    db_client = DBClient.new_db_client()
    try:
        total_songs = db_client.total_songs()
        socket.emit("totalSongs", total_songs)
    except Exception as e:
        logger.error("Error connecting to DB", exc_info=e)

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

        # matches, _, err = find_matches_fgp(fingerprint)
        # Dg
        matches, _, err = FindMatchesFGP(fingerprint)
        if err:
            logger.error("Failed to get matches", exc_info=err)
            return

        json_data = json.dumps([match.__dict__ for match in (matches[:10] if len(matches) > 10 else matches)])
        socket.emit("matches", json_data)
    except Exception as e:
        logger.error("Failed to handle new fingerprint", exc_info=e)
