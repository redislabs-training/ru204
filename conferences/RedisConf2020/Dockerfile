# redisuniversity/redisconf-2020
FROM redislabs/redisgraph:latest as redisgraph
FROM redislabs/redistimeseries:latest as redistimeseries
FROM redislabs/rejson:latest as rejson
FROM redislabs/rebloom:latest as rebloom
FROM redislabs/redisearch:1.6.10 as redisearch
FROM redisuniversity/virtual-lab-ide6:latest

ENV LD_LIBRARY_PATH /usr/lib/redis/modules

RUN set -ex && \
    apk add --no-cache libgomp

# Install RediSearch
COPY --from=redisearch ${LD_LIBRARY_PATH}/redisearch.so ${LD_LIBRARY_PATH}/

# Install Redis Gears

# Install RedisTimeSeris
COPY --from=redistimeseries ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install RedisJSON
COPY --from=rejson ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install RedisBloom
COPY --from=rebloom ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install Redis Graph
COPY --from=redisgraph ${LD_LIBRARY_PATH}/redisgraph.so ${LD_LIBRARY_PATH}/

# Install Sqlite for the Redis Gears Demo

# Course files
ADD .logo /home/student/.logo

# Set permissions
RUN chown -R student:student /src/redisu
RUN chown    student:student /home/student/.logo

# Supervisord config
ADD supervisord.conf /etc/
