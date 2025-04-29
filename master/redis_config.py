import redis
import os

def get_redis_connection():
    host = os.getenv("REDIS_HOST", "redis")
    port = os.getenv("REDIS_PORT", "6379")
    port = int(port.split(":")[-1])
    
    return redis.Redis(
        host=host,
        port=port,
        decode_responses=True
    )
