import os
import shutil
import struct
from typing import List

def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def create_folder(folder_path: str) -> None:
    os.makedirs(folder_path, exist_ok=True)


def move_file(source_path: str, destination_path: str) -> None:
    shutil.copy(source_path, destination_path)
    os.remove(source_path)


def floats_to_bytes(data: List[float], bits_per_sample: int) -> bytes:
    byte_data = []

    if bits_per_sample == 8:
        for sample in data:
            val = int((sample + 1.0) * 127.5)
            byte_data.append(struct.pack('B', val))
    elif bits_per_sample == 16:
        for sample in data:
            val = int(sample * 32767.0)
            byte_data.append(struct.pack('<h', val))
    elif bits_per_sample == 24:
        for sample in data:
            val = int(sample * 8388607.0)
            byte_data.append(struct.pack('<i', val)[1:])  # Keep only the lowest 3 bytes for 24-bit
    elif bits_per_sample == 32:
        for sample in data:
            val = int(sample * 2147483647.0)
            byte_data.append(struct.pack('<i', val))
    else:
        raise ValueError(f"Unsupported bitsPerSample: {bits_per_sample}")

    return b''.join(byte_data)
