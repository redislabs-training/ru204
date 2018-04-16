from redis import StrictRedis
import os

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
										port=os.environ.get("REDIS_PORT", 6379),
										db=0)


print redis.get("hello")