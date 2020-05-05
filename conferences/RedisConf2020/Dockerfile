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
      cmake

# INSTALL RediSearch
#RUN set -ex && \

# INSTALL Redis Gears
#RUN set -ex && \

# INSTALL RedisTimeSeris
#RUN set -ex && \

# INSTALL RedisJSON
#RUN set -ex && \

# INSTALL Redis Graph
#RUN set -ex && \

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
    apk del git make gcc linux-headers musl-dev cmake m4

# Course files
ADD .logo /home/student/.logo

# Set permissions
RUN chown -R student:student /src/redisu
RUN chown    student:student /home/student/.logo

# Supervisord config
ADD supervisord.conf /etc/
