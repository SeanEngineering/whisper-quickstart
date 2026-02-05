from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.redis_index import redis_client, index
from app.embeddings import embed
from app.whisper_service import transcribe
from app.utils import extract_audio
from app.models import SearchRequest
from redisvl.query import VectorQuery, FilterQuery, TextQuery
import uuid

app = FastAPI(title="Video Semantic Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    query_vec_bytes = embed(req.query)

    k = req.k if req.k is not None else 3

    q = VectorQuery(
        vector=query_vec_bytes,
        vector_field_name="embedding",
        num_results=k,
        return_fields=["content", "start", "end",
                       "vector_distance"]
    )

    results = index.query(q)

    print("Redis search results:", results)

    return [
        {
            "content": r["content"],
            "start": float(r["start"]),
            "end": float(r["end"]),
            "score": float(r["vector_distance"])
        }
        for r in results
    ]


@app.get("/videos/all")
def get_all():
    raw = redis_client.execute_command(
        "FT.SEARCH", "docs", "*",
        "RETURN", 3, "content", "start", "end",
        "LIMIT", 0, 1000
    )

    count = raw[0]
    entries = raw[1:]

    results = []
    for i in range(0, len(entries), 2):
        doc_id = entries[i]
        fields = entries[i + 1]

        it = iter(fields)
        obj = {"id": doc_id}
        for field, val in zip(it, it):
            obj[field] = val

        obj["start"] = float(obj.get("start", 0))
        obj["end"] = float(obj.get("end", 0))
        results.append(obj)

    return results
