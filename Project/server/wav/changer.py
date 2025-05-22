import os
import subprocess
import shutil
from utils.helpers import move_file

def convert_to_wav(input_file_path, channels):
    if not os.path.exists(input_file_path):
        raise ValueError(f"Input file does not exist: {input_file_path}")
    
    if channels < 1 or channels > 2:
        channels = 1  # Default to mono if the channel count is invalid
    
    file_ext = os.path.splitext(input_file_path)[1]
    output_file = os.path.splitext(input_file_path)[0] + ".wav"
    
    # Output file may already exist, so we'll use a temporary file
    tmp_file = os.path.join(os.path.dirname(output_file), "tmp_" + os.path.basename(output_file))

    # FFmpeg command to convert audio to WAV
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-i", input_file_path,  # Input file
        "-c", "pcm_s16le",  # Audio codec (signed 16-bit PCM)
        "-ar", "44100",  # Sample rate (44.1kHz)
        "-ac", str(channels),  # Channels (mono or stereo)
        tmp_file  # Temporary output file
    ]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert to WAV: {e.stderr.decode()}")
    

    move_file(tmp_file, output_file)
    
    return output_file

def reformat_wav(input_file_path, channels):
    if channels < 1 or channels > 2:
        channels = 1  # Default to mono if the channel count is invalid
    
    file_ext = os.path.splitext(input_file_path)[1]
    output_file = os.path.splitext(input_file_path)[0] + "rfm.wav"
    
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-i", input_file_path,  # Input file
        "-c", "pcm_s16le",  # Audio codec (signed 16-bit PCM)
        "-ar", "44100",  # Sample rate (44.1kHz)
        "-ac", str(channels),  # Channels (mono or stereo)
        output_file  # Output file path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to reformat WAV: {e.stderr.decode()}")
    
    return output_file

