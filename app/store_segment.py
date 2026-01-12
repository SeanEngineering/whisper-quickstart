import numpy as np


def store_segment(video_id, segment_id, segment, embedding):
    key = f"vid:{video_id}:{segment_id}"

    redis_client.hset(key, mapping={
        "content": segment["text"],
        "start": segment["start"],
        "end": segment["end"],
        "embedding": np.array(embedding, dtype=np.float32).tobytes()
    })
