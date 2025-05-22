
import time
import math
import logging
from typing import List, Dict, Tuple
import db.genClient as dbClient
import utils.loggs as logg
import utils.utils as utils
import shazam.spectrogram as spectrogram1
import shazam.fingerprint as fingerprint
import params

# Constants
# targetZoneSize = 2

class Match:
    def __init__(self, song_id: int, song_title: str, song_artist: str, youtube_id: str, timestamp: int, score: float):
        self.song_id = song_id
        self.song_title = song_title
        self.song_artist = song_artist
        self.youtube_id = youtube_id
        self.timestamp = timestamp
        self.score = score


def FindMatches(audio_sample: List[float], audio_duration: float, sample_rate: int) -> Tuple[List[Match], float, Exception]:
    start_time = time.time()

    try:
        spectrogram = spectrogram1.Spectrogram(audio_sample, sample_rate)
    except Exception as err:
        return [], time.time() - start_time, f"failed to get spectrogram of samples: {err}"

    peaks = spectrogram1.ExtractPeaks(spectrogram, audio_duration)

    sample_fingerprint = fingerprint.Fingerprint(peaks, utils.generate_unique_id())
    sample_fingerprint_map = {address: couple.anchor_time_ms for address, couple in sample_fingerprint.items()}

    matches, _, err = FindMatchesFGP(sample_fingerprint_map)
    return matches, time.time() - start_time, err

def FindMatchesFGP(sample_fingerprint: Dict[int, int]) -> Tuple[List[Match], float, Exception]:
    start_time = time.time()
    logger = logg.get_logger()

    addresses = list(sample_fingerprint.keys())

    try:
        db_client = dbClient.new_db_client()

    except Exception as err:
        return [], time.time() - start_time, err

    try:
        m = db_client.get_couples(addresses)

    except Exception as err:
        return [], time.time() - start_time, err
    finally:
        db_client.close()

    matches = {}  # songID -> [(sampleTime, dbTime)]
    timestamps = {}  # songID -> earliest timestamp
    target_zones = {}  # songID -> timestamp -> count

    for address, couples in m.items():
        for couple in couples:
            # song_id = couple.SongID
            #Dg
            song_id = couple.song_id

            if song_id not in matches:
                matches[song_id] = []

            # matches[song_id].append([sample_fingerprint[address], couple.AnchorTimeMs])
            # Dg
            matches[song_id].append([sample_fingerprint[address], couple.anchor_time_ms])

            # Update the earliest timestamp
            if song_id not in timestamps or couple.anchor_time_ms < timestamps[song_id]:
                timestamps[song_id] = couple.anchor_time_ms

            if song_id not in target_zones:
                target_zones[song_id] = {}

            # if couple.AnchorTimeMs not in target_zones[song_id]:
            if couple.anchor_time_ms not in target_zones[song_id]:
                target_zones[song_id][couple.anchor_time_ms] = 0

            target_zones[song_id][couple.anchor_time_ms] += 1

    # Optionally, filter matches
    matches = filter_matches(params.threshold, matches, target_zones,params.targetZoneSize2)

    scores = analyze_relative_timing(matches)

    match_list = []

    for song_id, points in scores.items():
        db_client=dbClient.new_db_client()
        song, song_exists= db_client.get_song_by_id(song_id)

        if not song_exists:
            logger.info(f"song with ID ({song_id}) doesn't exist")
            continue
        match = Match(song_id, song.title, song.artist, song.youtube_id, timestamps[song_id], points)
        match_list.append(match)

    match_list.sort(key=lambda x: x.score, reverse=True)

    return match_list, time.time() - start_time, None


def filter_matches(threshold: int, matches: Dict[int, List[Tuple[int, int]]], target_zones: Dict[int, Dict[int, int]], targetZoneSize2) -> Dict[int, List[Tuple[int, int]]]:
    # Filter out non target zones that don't meet the target zone size threshold
    for song_id, anchor_times in list(target_zones.items()):
        for anchor_time, count in list(anchor_times.items()):
            if count < targetZoneSize2:
                del target_zones[song_id][anchor_time]

    filtered_matches = {}
    for song_id, zones in target_zones.items():
        if len(zones) >= threshold:
            filtered_matches[song_id] = matches[song_id]

    return filtered_matches


def analyze_relative_timing(matches: Dict[int, List[Tuple[int, int]]]) -> Dict[int, float]:
    scores = {}
    for song_id, times in matches.items():
        count = 0
        for i in range(len(times)):
            for j in range(i + 1, len(times)):
                sample_diff = abs(times[i][0] - times[j][0])
                db_diff = abs(times[i][1] - times[j][1])
                # if abs(sample_diff - db_diff) < 100:  # Allow some tolerance
                if abs(sample_diff - db_diff) <params.tolerance:  # Allow some tolerance
                    count += 1
        scores[song_id] = float(count)
    return scores

# def analyze_relative_timing(matches: Dict[int, List[Tuple[int, int]]]) -> Dict[int, float]:
#     scores = {}
#     for song_id, time_pairs in matches.items():
#         offset_counts = {}  # offset -> count

#         for sample_time, db_time in time_pairs:
#             offset = abs(db_time - sample_time)
#             if offset in offset_counts:
#                 offset_counts[offset] += 1
#             else:
#                 offset_counts[offset] = 1

#         # Find the offset with the maximum count
#         max_count = 0

#         for count in offset_counts.values():
#             if count > max_count:
#                 max_count = count

#         scores[song_id] = float(max_count)

#     return scores

