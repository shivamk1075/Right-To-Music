
class Couple:
    def __init__(self, anchor_time_ms: int, song_id: int):
        self.anchor_time_ms = anchor_time_ms
        self.song_id = song_id

    def __repr__(self):
        return f"Couple(anchor_time_ms={self.anchor_time_ms}, song_id={self.song_id})"

class RecordData:

    def __init__(self, audio: str, duration: float, channels: int, sampleRate: int, sampleSize: int):
        self.audio = audio
        self.duration = duration
        self.channels = channels
        # Dg
        self.sampleRate = sampleRate
        self.sampleSize = sampleSize

    def __repr__(self):
        return (f"RecordData(audio={self.audio}, duration={self.duration}, channels={self.channels}, "
                f"sample_rate={self.sample_rate}, sample_size={self.sample_size})")
