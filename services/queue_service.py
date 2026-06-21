from rq import Queue
from core import redis_client

audio_to_text_queue=Queue("Voice to Text Queue",connection=redis_client)

