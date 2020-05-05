# redisuniversity/redisconf-2020
FROM redisuniversity/virtual-lab-base-6:latest

ENV LD_LIBRARY_PATH /usr/lib/redis/modules/

RUN set -ex && \
    apk add --no-cache \
      coreutils \
      g++ \
      linux-headers \
      m4 \
      make \
      musl-dev \
      libc6-compat \
      git \
      cmake \
      automake \
      autoconf

# INSTALL RediSearch
#RUN set -ex && \

# INSTALL Redis Gears
#RUN set -ex && \

# INSTALL RedisTimeSeris
#RUN set -ex && \

# INSTALL RedisJSON
RUN set -ex && \
    mkdir -p /usr/src/redisjson && \
    cd /usr/src/redisjson && \
    git clone https://github.com/RedisJSON/RedisJSON.git && \
    cd RedisJSON && \
    git checkout v1.0.4 && \
    make && \
    mkdir -p /usr/lib/redis/modules && \
    cp src/rejson.so /usr/lib/redis/modules && \
    cd /usr  && \
    rm -r /usr/src/redisjson

# INSTALL Redis Graph
# RUN set -ex && \
#     mkdir -p /usr/src/redisgraph && \
#     cd /usr/src/redisgraph && \
#     git clone --recurse-submodules -j8 https://github.com/RedisGraph/RedisGraph.git && \
#     cd RedisGraph && \
#     git checkout v2.0.11 -b 2.0.11 && \
#     make && \
#     mkdir -p /usr/lib/redis/modules && \
#     cp ./src/redisgraph.so /usr/lib/redis/modules

# INSTALL RedisBloom
RUN set -ex && \
    mkdir -p /usr/src/redisbloom && \
    cd /usr/src/redisbloom/ && \
    git clone https://github.com/RedisBloom/RedisBloom.git && \
    cd RedisBloom && \
    git checkout tags/v2.2.2 -b 2.2.2 && \
    make && \
    mkdir -p /usr/lib/redis/modules && \
    cp redisbloom.so /usr/lib/redis/modules

# Install Sqlite for the Redis Gears Demo

# CLEANUP
RUN set -ex && \
    apk del git make gcc linux-headers musl-dev cmake m4 automake autoconf

# Course files
ADD .logo /home/student/.logo

# Set permissions
RUN chown -R student:student /src/redisu
RUN chown    student:student /home/student/.logo

# Supervisord config
ADD supervisord.conf /etc/
