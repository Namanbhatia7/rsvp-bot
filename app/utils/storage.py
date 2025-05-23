import redis
import json

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

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

redis_client = RedisClient(host='localhost', port=6379, db=0)