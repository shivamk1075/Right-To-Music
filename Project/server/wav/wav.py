


import os
import json
import struct
import base64
import time
import json
import subprocess
from io import BytesIO


class WavHeader:
    def __init__(self, chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
                 num_channels, sample_rate, bytes_per_sec, block_align, bits_per_sample,
                 subchunk2_id, subchunk2_size):
        self.chunk_id = chunk_id
        self.chunk_size = chunk_size
        self.format = format
        self.subchunk1_id = subchunk1_id
        self.subchunk1_size = subchunk1_size
        self.audio_format = audio_format
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.bytes_per_sec = bytes_per_sec
        self.block_align = block_align
        self.bits_per_sample = bits_per_sample
        self.subchunk2_id = subchunk2_id
        self.subchunk2_size = subchunk2_size

    def to_bytes(self):
        return struct.pack('<4sI4s4sIHHIIHH4sI', self.chunk_id, self.chunk_size, self.format,
                           self.subchunk1_id, self.subchunk1_size, self.audio_format,
                           self.num_channels, self.sample_rate, self.bytes_per_sec,
                           self.block_align, self.bits_per_sample, self.subchunk2_id,
                           self.subchunk2_size)


def write_wav_header(f, data, sample_rate, channels, bits_per_sample):
    # Validate input
    if len(data) % channels != 0:
        raise ValueError("Data size not divisible by channels")

    # Calculate derived values
    subchunk1_size = 16  # Assuming PCM format
    bytes_per_sample = bits_per_sample // 8
    block_align = channels * bytes_per_sample
    subchunk2_size = len(data)

    # Build WAV header
    header = WavHeader(
        chunk_id=b'RIFF',
        chunk_size=36 + len(data),
        format=b'WAVE',
        subchunk1_id=b'fmt ',
        subchunk1_size=subchunk1_size,
        audio_format=1,  # PCM format
        num_channels=channels,
        sample_rate=sample_rate,
        bytes_per_sec=sample_rate * channels * bytes_per_sample,
        block_align=block_align,
        bits_per_sample=bits_per_sample,
        subchunk2_id=b'data',
        subchunk2_size=subchunk2_size
    )

    # Write header to file
    f.write(header.to_bytes())


def write_wav_file(filename, data, sample_rate, channels, bits_per_sample):
    with open(filename, 'wb') as f:
        if sample_rate <= 0 or channels <= 0 or bits_per_sample <= 0:
            raise ValueError("Values must be greater than zero")
        
        write_wav_header(f, data, sample_rate, channels, bits_per_sample)
        f.write(data)


# def read_wav_info(filename):
#     with open(filename, 'rb') as f:
#         data = f.read()
    
#     if len(data) < 44:
#         raise ValueError("Invalid WAV file size (too small)")

#     # Read header chunks
#     header = struct.unpack('<4sI4s4sIHHIIHH4sI', data[:44])
#     chunk_id = header[0]
#     format = header[2]
#     audio_format = header[5]
    
#     if chunk_id != b'RIFF' or format != b'WAVE' or audio_format != 1:
#         raise ValueError("Invalid WAV header format")

#     channels = header[6]
#     sample_rate = header[7]
#     data_chunk = data[44:]

#     # Calculate audio duration (assuming data contains PCM data)
#     if header[9] == 16:  # 16-bit PCM
#         duration = len(data_chunk) / (channels * 2 * sample_rate)
#     else:
#         print("DEBUG: bits_per_sample =", header[9])
#         raise ValueError("Unsupported bits per sample format")

#     return {
#         'channels': channels,
#         'sample_rate': sample_rate,
#         'data': data_chunk,
#         'duration': duration
#     }
# Dg
import struct

def read_wav_info(filename):
    with open(filename, 'rb') as f:
        riff = f.read(12)
        if riff[0:4] != b'RIFF' or riff[8:12] != b'WAVE':
            raise ValueError("Invalid WAV header")

        fmt_chunk_found = False
        data_chunk_found = False
        sample_rate = None
        channels = None
        bits_per_sample = None
        data_size = None

        while True:
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break
            chunk_id, chunk_size = struct.unpack('<4sI', chunk_header)

            if chunk_id == b'fmt ':
                fmt_chunk_found = True
                fmt_data = f.read(chunk_size)
                (
                    audio_format,
                    channels,
                    sample_rate,
                    byte_rate,
                    block_align,
                    bits_per_sample
                ) = struct.unpack('<HHIIHH', fmt_data[:16])
                if audio_format != 1:
                    raise ValueError("Only PCM WAV files supported")
            elif chunk_id == b'data':
                data_chunk_found = True
                data_size = chunk_size

                # Dg
                data = f.read(chunk_size)  # <--- Add this line
                break  # We got what we need
            else:
                # Skip unknown chunks
                f.seek(chunk_size, 1)

        if not (fmt_chunk_found and data_chunk_found):
            raise ValueError("Missing required chunks")

        duration = data_size / (sample_rate * channels * (bits_per_sample / 8))

        return {
            'channels': channels,
            'sample_rate': sample_rate,
            'bits_per_sample': bits_per_sample,
            'duration': duration,
            
            # Dg
            'data': data  # <-- Add this line
        }


def wav_bytes_to_samples(input_bytes):
    if len(input_bytes) % 2 != 0:
        raise ValueError("Invalid input length")

    num_samples = len(input_bytes) // 2
    output = []

    for i in range(0, len(input_bytes), 2):
        sample = struct.unpack('<h', input_bytes[i:i+2])[0]
        output.append(sample / 32768.0)

    return output


class FFmpegMetadata:
    def __init__(self):
        self.streams = []
        self.format = {}

    def from_json(self, json_data):
        data = json.loads(json_data)
        self.streams = data.get('streams', [])
        self.format = data.get('format', {})

# New func 0
def get_metadata(file_path):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams", file_path
    ]
    
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # print(f"Running command: {' '.join(cmd)}")
    if result.returncode != 0:
        print("ffprobe failed with stderr:")
        print(result.stderr.decode())
        raise Exception(f"Error getting metadata: {result.stderr.decode()}")

    # print("ffprobe output:")
    # print(result.stdout.decode()[:500])  # Only print the first 500 chars

    metadata = FFmpegMetadata()
    metadata.from_json(result.stdout.decode())
    
    return metadata,None

# def get_metadata(file_path):
#     cmd = [
#         "ffprobe",
#         "-v", "quiet",
#         "-print_format", "json",
#         "-show_format", "-show_streams", file_path
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
#     if result.returncode != 0:
#         raise Exception(f"Error getting metadata: {result.stderr.decode()}")

#     metadata = FFmpegMetadata()
#     metadata.from_json(result.stdout.decode())
    
#     return metadata

# New Func is written here 1
# def get_metadata(file_path):
#     cmd = [
#         "ffprobe",
#         "-v", "quiet",
#         "-print_format", "json",
#         "-show_format", "-show_streams", file_path
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     print("stdout:", result.stdout.decode())  # Print the stdout to see raw JSON output
#     print("stderr:", result.stderr.decode())  # Print stderr to check for any errors

#     if result.returncode != 0:
#         raise Exception(f"Error getting metadata: {result.stderr.decode()}")

#     # metadata = FFmpegMetadata()
#     # metadata.from_json(result.stdout.decode())
    
#     # return metadata

#     # For now modifying above
#     metadata = json.loads(result.stdout.decode())
#     return metadata
# New func 3
# def get_metadata(file_path):
#     # Run ffprobe and collect output
#     cmd = [
#         "ffprobe",
#         "-v", "quiet",
#         "-print_format", "json",
#         "-show_format", "-show_streams", file_path
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     if result.returncode != 0:
#         raise Exception(f"Error getting metadata: {result.stderr.decode()}")

#     # Load JSON output from ffprobe
#     raw_metadata = json.loads(result.stdout.decode())

#     # Convert all Tags keys to lowercase
#     if "format" in raw_metadata and "tags" in raw_metadata["format"]:
#         raw_metadata["format"]["tags"] = {
#             k.lower(): v for k, v in raw_metadata["format"]["tags"].items()
#         }

#     if "streams" in raw_metadata and len(raw_metadata["streams"]) > 0:
#         if "tags" in raw_metadata["streams"][0]:
#             raw_metadata["streams"][0]["tags"] = {
#                 k.lower(): v for k, v in raw_metadata["streams"][0]["tags"].items()
#             }

#     # Convert to FFmpegMetadata object if needed
#     metadata = FFmpegMetadata()
#     metadata.from_json(json.dumps(raw_metadata))

#     return metadata


def process_recording(rec_data, save_recording):
    decoded_audio_data = base64.b64decode(rec_data['audio'])

    now = time.localtime()
    file_name = f"{now.tm_sec}_{now.tm_min}_{now.tm_hour}_{now.tm_mday}_{now.tm_mon}_{now.tm_year}.wav"
    file_path = f"tmp/{file_name}"

    write_wav_file(file_path, decoded_audio_data, rec_data['sample_rate'], rec_data['channels'], rec_data['sample_size'])

    reformatted_wav_file = reformat_wav(file_path, 1)

    wav_info = read_wav_info(reformatted_wav_file)
    samples = wav_bytes_to_samples(wav_info['data'])

    if save_recording:
        os.makedirs("recordings", exist_ok=True)
        new_file_path = reformatted_wav_file.replace("tmp/", "recordings/")
        os.rename(reformatted_wav_file, new_file_path)

    os.remove(file_path)
    os.remove(reformatted_wav_file)

    return samples


def reformat_wav(input_file, channels):
    # Assuming that FFmpeg is used for reformatting
    output_file = input_file.replace('.wav', '_rfm.wav')
    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-ac', str(channels), output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file
