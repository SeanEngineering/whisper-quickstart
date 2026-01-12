from fastapi import FastAPI, UploadFile, File
from app.redis_index import redis_client, index
from app.embeddings import embed
from app.whisper_service import transcribe
from app.utils import extract_audio
from app.models import SearchRequest
from redisvl.query import VectorQuery
import uuid

app = FastAPI(title="Video Semantic Search API")


@app.post("/videos/embed")
async def embed_video(file: UploadFile = File(...)):
    video_bytes = await file.read()
    audio_path = extract_audio(video_bytes)
    segments = transcribe(str(audio_path))

    video_id = str(uuid.uuid4())

    for i, seg in enumerate(segments):
        redis_client.hset(
            f"vid:{video_id}:{i}",
            mapping={
                "content": seg["text"],
                "start": seg["start"],
                "end": seg["end"],
                "embedding": embed(seg["text"])
            }
        )

    return {
        "video_id": video_id,
        "segments_indexed": len(segments)
    }


@app.post("/videos/search")
def search(req: SearchRequest):
    query_vec = embed(req.query)

    q = VectorQuery(
        vector=query_vec,
        vector_field_name="embedding",
        num_results=req.k,
        return_fields=["content", "start", "end"]
    )

    results = index.query(q)

    return [
        {
            "content": r["content"],
            "start": float(r["start"]),
            "end": float(r["end"]),
            "score": r["score"]
        }
        for r in results
    ]
