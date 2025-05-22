# This file is the main entry point for the CLI=RIGHT-TO-MUSIC application.

import sys
import argparse
from utils.loggs import get_logger
from utils.helpers import create_folder
import CMD

SONGS_DIR = "songs"

def main():
    logger = get_logger()
    
    for folder in ["tmp", SONGS_DIR]:
        try:
            create_folder(folder)
        except Exception as e:
            logger.error(f"Failed to create directory '{folder}': {e}")

    parser = argparse.ArgumentParser(description="CLI=RIGHT-TO-MUSIC")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # find command
    find_parser = subparsers.add_parser("find", help="Find songs from file path")
    find_parser.add_argument("file_path", type=str, help="Path to file")

    # download command
    download_parser = subparsers.add_parser("download", help="Download songs from Spotify URL")
    download_parser.add_argument("spotify_url", type=str, help="Spotify URL")

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start the server")
    serve_parser.add_argument("--proto", type=str, default="http", help="Protocol (http or https)")
    serve_parser.add_argument("-p", "--port", type=str, default="5000", help="Port number")

    # erase command
    erase_parser = subparsers.add_parser("erase", help="Erase downloaded songs")

    eraseID_parser=subparsers.add_parser("eraseID", help="Erase downloaded songs by id")
    eraseID_parser.add_argument("SongID", type=str, help="Song ID to erase")

    # save command
    save_parser = subparsers.add_parser("save", help="Save WAV files metadata")
    save_parser.add_argument("file_path", type=str, help="File or directory path")
    save_parser.add_argument("-f", "--force", action="store_true", help="Force save without YouTube ID")

    args = parser.parse_args()

    # Dispatch commands
    if args.command == "find":
        CMD.find(args.file_path)
    elif args.command == "download":
        CMD.download(args.spotify_url)
    elif args.command == "serve":
        CMD.serve(args.proto, args.port)
    elif args.command == "erase":
        CMD.erase(SONGS_DIR)
    elif args.command == "eraseID":
        CMD.eraseID(SONGS_DIR,args.SongID)
    elif args.command == "save":
        CMD.save(args.file_path, args.force)


if __name__ == "__main__":
    main()



