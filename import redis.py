import redis 

redis_client = redis.Redis(host= "localhost", port=6378)

print(redis_client.ping())