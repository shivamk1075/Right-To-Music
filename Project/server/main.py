

import sys
import argparse
from utils.logger import get_logger
from utils.helpers import create_folder
import cmdHandlers as cmdHandlers  

# //db downloading
import os
import urllib.request

# Ensuring DB is present
def download_db_if_missing():
    db_folder = "db"
    db_filename = "db.sqlite3"
    db_path = os.path.join(db_folder, db_filename)

    db_url = "https://drive.google.com/uc?export=download&id=1vj43ObRbVrBW6eU7gumGtt9EfbZw0gQn"

    os.makedirs(db_folder, exist_ok=True)

    if not os.path.exists(db_path):
        print("Downloading database...")
        urllib.request.urlretrieve(db_url, db_path)
        print("Download complete.")

download_db_if_missing()
# //

SONGS_DIR = "songs"

def main():
    logger = get_logger()
    

    for folder in ["tmp", SONGS_DIR]:
        try:
            create_folder(folder)
        except Exception as e:
            logger.error(f"Failed to create directory '{folder}': {e}")

    parser = argparse.ArgumentParser(description="Musical_Spark _CLI_")
    subparsers = parser.add_subparsers(dest="command", required=True)


    find_parser = subparsers.add_parser("find", help="Find songs from file path")
    find_parser.add_argument("file_path", type=str, help="Path to file")


    download_parser = subparsers.add_parser("download", help="Download songs from Spotify URL")
    download_parser.add_argument("spotify_url", type=str, help="Spotify URL")


    serve_parser = subparsers.add_parser("serve", help="Start the server")
    serve_parser.add_argument("--proto", type=str, default="http", help="Protocol (http or https)")
    serve_parser.add_argument("-p", "--port", type=str, default="5000", help="Port number")


    erase_parser = subparsers.add_parser("erase", help="Erase downloaded songs")

    eraseID_parser=subparsers.add_parser("eraseID", help="Erase downloaded songs by id")
    eraseID_parser.add_argument("SongID", type=str, help="Song ID to erase")


    save_parser = subparsers.add_parser("save", help="Save WAV files metadata")
    save_parser.add_argument("file_path", type=str, help="File or directory path")
    save_parser.add_argument("-f", "--force", action="store_true", help="Force save without YouTube ID")

    args = parser.parse_args()


    if args.command == "find":
        cmdHandlers.find(args.file_path)
    elif args.command == "download":
        cmdHandlers.download(args.spotify_url)
    elif args.command == "serve":
        cmdHandlers.serve(args.proto, args.port)
    elif args.command == "erase":
        cmdHandlers.erase(SONGS_DIR)
    elif args.command == "eraseID":
        cmdHandlers.eraseID(SONGS_DIR,args.SongID)
    elif args.command == "save":
        cmdHandlers.save(args.file_path, args.force)


if __name__ == "__main__":
    main()



