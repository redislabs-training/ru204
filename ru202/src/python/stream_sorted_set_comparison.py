import sys
from util.connection import get_connection

STREAM_KEY = 'ru202:demo:stream'
SORTED_SET_KEY = 'ru202:demo:sortedset'

def setup():
    # Removes any pre-existing Stream and Sorted Set
    redis = get_connection()
    redis.delete(STREAM_KEY)
    redis.delete(SORTED_SET_KEY)

def producer(numToProduce):
    print(f'Producing {numToProduce} items.')

    redis = get_connection()

    for n in range(1, numToProduce + 1):
        message = f'hello{n}'

        # Add to stream, h here is the identifier.
        redis.xadd(STREAM_KEY, {'m': message}, n)

        # Add to sorted set, n here is the score.
        redis.zadd(SORTED_SET_KEY, {message: n})

def memoryUsage():
    redis = get_connection()

    streamMemoryUsage = redis.memory_usage(STREAM_KEY, 0)
    sortedSetMemoryUsage = redis.memory_usage(SORTED_SET_KEY, 0)

    print(f'Stream memory usage:     {streamMemoryUsage}')
    print(f'Sorted set memory usage: {sortedSetMemoryUsage}')
    print(f'Difference:              {sortedSetMemoryUsage - streamMemoryUsage}')

    diff = sortedSetMemoryUsage / streamMemoryUsage
    print(f'Sorted set bigger by:    {format(diff, ".2f")}x')

if __name__ == '__main__':
    setup()

    numToProduce = 10000

    if len(sys.argv) == 2:
        try:
            numToProduce = int(sys.argv[1])
        except ValueError:
            sys.exit(f'Usage {sys.argv[0]} <number of messages>')

    producer(numToProduce)
    memoryUsage()