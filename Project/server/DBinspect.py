#  This script connects to a SQLite database, retrieves song information, and saves it to an Excel file.

import sqlite3
from openpyxl import Workbook

conn = sqlite3.connect("db/db.sqlite3")
cursor = conn.cursor()

print("\n--- Songs in Database ---\n")

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Songs"

# Write headers
headers = ["ID", "Title", "Artist", "YouTube ID", "YouTube Link", "Fingerprints"]
ws.append(headers)

cursor.execute("SELECT id, title, artist, ytID FROM songs")
songs = cursor.fetchall()

for song in songs:
    song_id, title, artist, yt_id = song
    cursor.execute("SELECT COUNT(*) FROM fingerprints WHERE songID = ?", (song_id,))
    fingerprint_count = cursor.fetchone()[0]

    print(f"ID: {song_id}")
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"YouTube ID: {yt_id}")
    print(f"YouTube link: https://www.youtube.com/watch?v={yt_id}")
    print(f"Fingerprints: {fingerprint_count}")
    print("-" * 40)

    # Append the data row to the Excel worksheet
    ws.append([
        song_id,
        title,
        artist,
        yt_id,
        f"https://www.youtube.com/watch?v={yt_id}",
        fingerprint_count
    ])

conn.close()

# Save the workbook
wb.save("songs.xlsx")
