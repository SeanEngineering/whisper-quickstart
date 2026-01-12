import subprocess
import uuid
from pathlib import Path

TMP_DIR = Path("/tmp/videos")
TMP_DIR.mkdir(exist_ok=True)


def extract_audio(video_bytes: bytes) -> Path:
    video_path = TMP_DIR / f"{uuid.uuid4()}.mp4"
    audio_path = TMP_DIR / f"{uuid.uuid4()}.wav"

    video_path.write_bytes(video_bytes)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-ar", "16000",
        "-ac", "1",
        str(audio_path)
    ], check=True)

    return audio_path
