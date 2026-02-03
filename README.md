# Using Whisper AI for Video Embeddings
Whisper is speech recognition model developer by Open AI back in 2022. This can be combined with RedisVL to create a model 

This application uses ffmpeg so make sure to install this before running the model.

```shell
  brew install ffmpeg
```
## Setup Python App
Note that you will need to use a Python version between 3.9 and 3.14
```shell
  python3.11 -m venv .venv
```

```shell
source ./.venv/bin/activate
```

Download the python packages
```shell
  pip install -r requirements.txt
```

## Setup and Run Redis via Docker
Run a Redis instance locally using the following command
```shell
  docker run -d --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## Run Python App
```shell
  python -m uvicorn app.main:app --reload
```
## Next Steps
Video frames will be analysed using an OCR in future at a sampling rate of 1 FPS.

