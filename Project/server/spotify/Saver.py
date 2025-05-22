from .getYT import get_youtube_id
from .TrackClass import Track
from utils.loggs import get_logger
import wav.wavFuncs as wavFuncs
import wav.changer as changer
from shazam.spectrogram import Spectrogram, ExtractPeaks
from shazam.fingerprint import Fingerprint
from db.genClient import new_db_client
from .Helps import yt_id_exists, song_key_exists
import params

logger = get_logger()
DELETE_SONG_FILE = False

def process_and_save_song(wav_path: str, title: str, artist: str, yt_id: str) -> bool:

    db = new_db_client()   
    wav_info = wavFuncs.read_wav_info(wav_path)
    samples = wavFuncs.wav_bytes_to_samples(wav_info['data'])
    spectro = Spectrogram(samples, wav_info['sample_rate'])

    try:
        song_id = db.register_song(title, artist, yt_id)
    except ValueError as e:
        print(f"[INFO] {e}")
        return None  # or return an existing song ID from a lookup

    peaks = ExtractPeaks(spectro, wav_info['duration'])
    fingerprints = Fingerprint(peaks, song_id)
    if not db.store_fingerprints(fingerprints):
        db.delete_song_by_id(song_id)
        return False
    print(f"Fingerprint for {title} by {artist} saved in DB successfully")
    return True

def get_yt_id(track: Track) -> str:
    yt_id = get_youtube_id(track)
    if not yt_id or yt_id_exists(yt_id):
        yt_id = get_youtube_id(track)
        if not yt_id or yt_id_exists(yt_id):
            return ""
    return yt_id
