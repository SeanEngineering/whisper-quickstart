import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")


def embed(text: str) -> bytes:
    vec = model.encode(text, normalize_embeddings=True)
    return np.array(vec, dtype=np.float32).tobytes()
