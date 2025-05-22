import os
import shutil
from pathlib import Path
import socketio
import Sockets
import wav.wavFuncs as wavFuncs
import wav.changer as changer
import shazam.MainShazam as MainShazam
import spotify.TrackClass as TrackClass
import spotify.Saver as Saver
import spotify.getYT as getYT
import db.genClient as genClient
import utils.loggs as logg
import utils.helpers as helpers
import eventlet
import eventlet.wsgi
import ssl

SONGS_DIR = "songs"
yellow = logg.get_logger()

def find_song(file_path: str):


    wav_file = changer.convert_to_wav(file_path, channels=1)
    wav_info= wavFuncs.read_wav_info(wav_file)
    samples= wavFuncs.wav_bytes_to_samples(wav_info["data"])
    matches, search_duration, err = MainShazam.FindMatches(samples, wav_info["duration"], wav_info["sample_rate"])
    os.remove(wav_file)
    if err:
        yellow.error("Error finding matches:", err)
        print(f"Error finding matches: {err}")
        return

    if not matches:
        print("\nNo match found.")
        print(f"\nSearch took: {search_duration}")
        return

    msg = "Matches:"
    top_matches = matches
    if len(matches) >= 20:
        msg = "Top 20 matches:"
        top_matches = matches[:20]

    print(msg)
    for match in top_matches:
        print(f"\t- {match.song_title} by {match.song_artist}, score: {match.score:.2f}")

    print(f"\nSearch took: {search_duration}")
    top_match = top_matches[0]
    print(f"\nFinal prediction: {top_match.song_title} by {top_match.song_artist} by {top_match.youtube_id}, score: {top_match.score:.2f}")
    print(f"https://www.youtube.com/watch?v={top_match.youtube_id}")


def find(file_path: str):
    if os.path.isdir(file_path):
        for file_name in os.listdir(file_path):
            full_file_path = os.path.join(file_path, file_name)
            if not os.path.isdir(full_file_path):
                ext = Path(file_name).suffix.lower()
                try:
                    print(f"\n Finding match for: {file_name}")
                    find_song(full_file_path)
                except Exception as e:
                    print(f"Exception while finding match for {full_file_path}: {e}")
    else:
        ext = Path(file_path).suffix.lower()
        try:
            print(f"\n Finding match for: {file_path}")
            find_song(file_path)
        except Exception as e:
            print(f"Exception while finding match for {file_path}: {e}")


def serve(protocol: str, port: str):
    protocol = protocol.lower()
    server = socketio.Server(cors_allowed_origins="*", async_mode="eventlet", transports=["websocket"])


    @server.event
    def connect(sid, environ):
        print(f"CONNECTED: {sid}")
        return True
    @server.event
    def totalSongs(sid,str):
        Sockets.handle_total_songs(server)


    @server.event
    def newRecording(sid, file_path):
        Sockets.handle_new_recording(server, file_path)

    @server.event
    def newFingerprint(sid, fingerprint_data):
        Sockets.handle_new_fingerprint(server, fingerprint_data)
    
    @server.event
    def recordedAudioData(sid, data):
        Sockets.handle_recorded_audio(server, sid, data)

    @server.event
    def disconnect(sid):
        print(f"DISCONNECTED: {sid}")

    if protocol == "https":
        serve_https(server, port)
    else:
        serve_http(server, port)


def serve_https(socket_server, port: str):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='/etc/letsencrypt/live/localport.online/fullchain.pem',
                            keyfile='/etc/letsencrypt/live/localport.online/privkey.pem')

    app = socketio.WSGIApp(socket_server)
    print(f"Starting HTTPS server on port {port}")
    eventlet.wsgi.server(eventlet.listen(('', int(port)), backlog=100), app, ssl_context=context)


def serve_http(socket_server, port: str):
    app = socketio.WSGIApp(socket_server)
    print(f"Starting HTTP server on port {port}")
    eventlet.wsgi.server(eventlet.listen(('', int(port)), backlog=100), app)


def erase(songs_dir: str):
    logger = logg.get_logger()
    ctx = None


    db_client = genClient.new_db_client()
    err = db_client.delete_collection("fingerprints")
    if err:
        logger.error(f"Error deleting collection: {err}", exc_info=err)

    err = db_client.delete_collection("songs")
    if err:
        logger.error(f"Error deleting collection: {err}", exc_info=err)

    try:
        for root, dirs, files in os.walk(songs_dir):
            for file in files:
                ext = Path(file).suffix
                if ext in [".wav", ".m4a"]:
                    os.remove(os.path.join(root, file))
    except Exception as err:
        logger.error(f"Error walking through directory {songs_dir}: {err}", exc_info=err)

    print("Erase complete")

def eraseID(songs_dir : str , SongID : str):
    logger = logg.get_logger()
    ctx = None

    db_client = genClient.new_db_client()
    err = db_client.delete_song_by_id(SongID)
    if err:
        logger.error(f"Error deleting song: {err}", exc_info=err)

    print(f"Erase complete for song id {SongID}")

def save(file_path: str, force: bool):
    if os.path.isdir(file_path):
        for file_name in os.listdir(file_path):
            full_file_path = os.path.join(file_path, file_name)
            if not os.path.isdir(full_file_path):
                try:
                    err = save_song(full_file_path, force)
                    if err:
                        print(f"Error saving song ({full_file_path}): {err}")
                except Exception as e:
                    print(f"Exception while saving {full_file_path}: {e}")
    else:
        try:
            err = save_song(file_path, force)
            if err:
                print(f"Error saving song ({file_path}): {err}")
        except Exception as e:
            print(f"Exception while saving {file_path}: {e}")



def save_song(input_path: str, force: bool) -> str:


    file_path=changer.convert_to_wav(input_path,1)

    metadata, err = wavFuncs.get_metadata(file_path)


    if err:
        return err

    try:

        duration_float = float(metadata.format["duration"])
    except ValueError:
        return f"Failed to parse duration to float: {metadata.format['duration']}"

    tags=metadata.format["tags"]
    track = TrackClass.Track(
        album=tags.get("album"),
        artist=tags.get("artist"),
        artists=tags.get("artists"),
        title=tags.get("title"),
        duration=int(round(duration_float))
    )

    yt_id = getYT.get_youtube_id(track)
    if yt_id is None and not force:
        print(f"Could not find a YouTube match for track: {track.title} by {track.artist}")
        return

    file_name = Path(file_path).stem
    if not track.title:
        track.title = file_name

    if not track.artist:
        return "No artist found in metadata"

    err = Saver.process_and_save_song(file_path, track.title, track.artist, yt_id)

    wav_file = f"{file_name}.wav"
    source_path = os.path.join(Path(file_path).parent, wav_file)
    new_file_path = os.path.join(SONGS_DIR, wav_file)
    if not err:
        os.remove(source_path)
        return f"Failed to process or save song: {err}"
    try:
        shutil.move(source_path, new_file_path)
    except Exception as err:
        return f"Failed to rename temporary file to output file: {err}"
    print("Saved the song successfully")

    return ""