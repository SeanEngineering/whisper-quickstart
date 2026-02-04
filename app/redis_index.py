# import redis
# from redisvl.schema import IndexSchema
# from redisvl.index import SearchIndex

# EMBEDDING_DIM = 768

# schema_dict = {
#     "name": "video_idx",
#     "prefix": "vid",
#     "storage_type": "hash",
#     "fields": [
#         {"name": "content", "type": "text"},
#         {"name": "start", "type": "numeric"},
#         {"name": "end", "type": "numeric"},
#         {
#             "name": "embedding",
#             "type": "vector",
#             "attrs": {
#                 "TYPE": "FLOAT32",
#                 "dims": EMBEDDING_DIM,
#                 "distance_metric": "COSINE"
#             }
#         }
#     ]
# }

# # Create IndexSchema from dictionary
# schema = IndexSchema.from_dict(schema_dict)

# # Create Redis client
# redis_client = redis.Redis(host="localhost", port=6379)

# # Create the search index
# index = SearchIndex(schema, redis_client)
# index.create(overwrite=False)
from redis import Redis
from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex

redis_client = Redis(host="localhost", port=6379, decode_responses=True)


schema = IndexSchema.from_dict({
    "index": {
        "name": "docs",
        "prefix": "vid:",
        "storage_type": "hash"
    },
    "fields": [
        {"name": "id", "type": "tag"},
        {"name": "content", "type": "text"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "algorithm": "HNSW",
                "dims": 768,
                "distance_metric": "cosine",
                "type": "FLOAT32"
            }
        }
    ]
})

index = SearchIndex(schema, redis_client)


def init_index():
    index.create(overwrite=True)


init_index()
