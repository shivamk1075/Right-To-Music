

import numpy as np
import params

# Constants
maxFreqBits = 9
maxDeltaBits = 14
# targetZoneSize1 = 5

class Peak:
    def __init__(self, time, freq):
        self.time = time  # Time in seconds
        self.freq = freq  # Frequency as complex number


class Couple:
    def __init__(self, anchor_time_ms, song_id):
        self.anchor_time_ms = anchor_time_ms  # Time in milliseconds
        self.song_id = song_id  # ID of the song


# Fingerprint function generates fingerprints from a list of peaks and stores them in a dictionary.
# Each fingerprint consists of an address and a couple.
# The address is a hash. The couple contains the anchor time and the song ID.
def Fingerprint(peaks, song_id):
    fingerprints = {}
    # print(params.targetZoneSize1)
    tZS1 = params.targetZoneSize1
    # print(f"targetZoneSize1 : {tZS1} and type : {type(tZS1)}")

    for i, anchor in enumerate(peaks):
        for j in range(i + 3, min(i + 3 + tZS1, len(peaks))):
        # for j in range(i + 3, min(i + targetZoneSize1, len(peaks))):
            target = peaks[j]

            # # Dg
            # print(type(anchor))
            # print(anchor)
            address = create_address(anchor, target)
            anchor_time_ms = int(anchor.time * 1000)
            # # Dg
            # anchor_time_ms = int(anchor['Time'] * 1000)

            fingerprints[address] = Couple(anchor_time_ms, song_id)

    return fingerprints


# create_address function generates a unique address for a pair of anchor and target points.
# The address is a 32-bit integer where certain bits represent the frequency of
# the anchor and target points, and other bits represent the time difference (delta time)
# between them. This function combines these components into a single address (a hash).
def create_address(anchor, target):
    anchor_freq = int(np.real(anchor.freq))  # Use real part of frequency
    target_freq = int(np.real(target.freq))  # Use real part of frequency
    delta_ms = int((target.time - anchor.time) * 1000)  # Time difference in milliseconds
    
    # # Dg
    # anchor_freq = int(np.real(anchor['Freq']))  # Use real part of frequency
    # target_freq = int(np.real(target['Freq']))  # Use real part of frequency
    # delta_ms = int((target['Time'] - anchor['Time']) * 1000)  # Time difference in milliseconds

    # Combine the frequency of the anchor, target, and delta time into a 32-bit address
    address = (anchor_freq << 23) | (target_freq << 14) | delta_ms

    # return address
    # Dg
    return int(address)


# # Example usage
# peaks = [Peak(0.0, 1000 + 10j), Peak(0.1, 1050 + 20j), Peak(0.2, 1100 + 30j)]  # Example peaks
# song_id = 12345
# fingerprints = Fingerprint(peaks, song_id)

# # Display fingerprints
# for address, couple in fingerprints.items():
#     print(f"Address: {address}, Time: {couple.anchor_time_ms}, Song ID: {couple.song_id}")
