import os
import subprocess
from urllib.parse import quote_plus
import sqlite3
from typing import Tuple

def encode_param(s: str) -> str:
    return quote_plus(s)

def to_lower_case(s: str) -> str:
    return s.lower()

def get_file_size(file: str) -> Tuple[int, str]:
    try:
        file_info = os.stat(file)
        return file_info.st_size, None
    except Exception as e:
        return 0, str(e)


def yt_id_exists(yt_id: str) -> Tuple[bool, str]:
    try:
        conn = sqlite3.connect('db.db')  # Change with your actual database path
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM songs WHERE yt_id=?", (yt_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists, None
    except Exception as e:
        return False, str(e)


def correct_filename(title: str, artist: str) -> Tuple[str, str]:
    invalid_chars = ['<', '>', ':', '"', '\\', '/', '|', '?', '*']
    for char in invalid_chars:
        title = title.replace(char, '')
        artist = artist.replace(char, '')
    
    title = title.replace("/", "\\")
    artist = artist.replace("/", "\\")
    
    return title, artist


def convert_stereo_to_mono(stereo_file_path: str) -> Tuple[bytes, str]:
    file_ext = os.path.splitext(stereo_file_path)[1]
    mono_file_path = stereo_file_path.replace(file_ext, "_mono" + file_ext)
    
    try:
        # Check the number of channels in the stereo audio
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'stream=channels', '-of', 'default=noprint_wrappers=1:nokey=1', stereo_file_path]
        output = subprocess.check_output(cmd)
        channels = output.decode().strip()

        if channels != "1":
            # Convert stereo to mono
            cmd = ['ffmpeg', '-i', stereo_file_path, '-af', 'pan=mono|c0=c0', mono_file_path]
            subprocess.run(cmd, check=True)
        
        with open(mono_file_path, 'rb') as f:
            audio_bytes = f.read()

        os.remove(mono_file_path)
        return audio_bytes, None
    
    except Exception as e:
        return b'', str(e)
