import os
import ssl
import redis
import json

class RedisClient:
    def __init__(self, host='localhost', port=6379, password=None, ssl=False, db=0, decoded_responses=True):
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            ssl=ssl,
            db=db,
            decode_responses=decoded_responses
        )

    def set(self, key, value):
        self.client.set(key, json.dumps(value))

    def get(self, key):
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None

    def delete(self, key):
        self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key)

redis_client = RedisClient(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    ssl=os.getenv("REDIS_SSL", False),
    db=0,
    decode_responses=True
)