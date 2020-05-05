# redisuniversity/virtual-lab-base-6
ARG ALPINE_VERSION=3.9

FROM alpine:$ALPINE_VERSION

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN addgroup -S redis && adduser -S -G redis redis

# grab su-exec for easy step-down from root
RUN apk add --no-cache 'su-exec>=0.2'

ARG REDIS_5_VERSION
ARG REDIS_5_DOWNLOAD_SHA
ARG REDIS_5_DOWNLOAD_URL

ARG REDIS_6_VERSION
ARG REDIS_6_DOWNLOAD_SHA
ARG REDIS_6_DOWNLOAD_URL

# for redis-sentinel see: http://redis.io/topics/sentinel
RUN set -ex && \
  	apk add --no-cache \
  		coreutils \
  		gcc \
      linux-headers \
  		make \
  		musl-dev \
      bash \
      supervisor \
      curl \
      git \
      vim \
      libc6-compat \
      nginx \
      libgit2-dev \
      build-base \
      zip \
      ttyd \
      cmake \
      dpkg \
      python3 \
      py-pip && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade --no-cache-dir redis==3.5.0

# Install Redis 5.x
RUN set -ex && \
  	wget -O redis.tar.gz "$REDIS_5_DOWNLOAD_URL" && \
  	echo "$REDIS_5_DOWNLOAD_SHA *redis.tar.gz" | sha256sum -c - && \
  	mkdir -p /usr/src/redis && \
  	tar -xzf redis.tar.gz -C /usr/src/redis --strip-components=1 && \
  	rm redis.tar.gz && \
# disable Redis protected mode [1] as it is unnecessary in context of Docker
# (ports are not automatically exposed when running inside Docker, but rather explicitly by specifying -p / -P)
# [1]: https://github.com/antirez/redis/commit/edd4d555df57dc84265fdfb4ef59a4678832f6da
  	grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 1$' /usr/src/redis/src/server.h && \
  	sed -ri 's!^(#define CONFIG_DEFAULT_PROTECTED_MODE) 1$!\1 0!' /usr/src/redis/src/server.h && \
  	grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 0$' /usr/src/redis/src/server.h && \
# for future reference, we modify this directly in the source instead of just supplying a default configuration flag because apparently "if you specify any argument to redis-server, [it assumes] you are going to specify everything"
# see also https://github.com/docker-library/redis/issues/4#issuecomment-50780840
# (more exactly, this makes sure the default behavior of "save on SIGTERM" stays functional by default)
  	make -C /usr/src/redis -j "$(nproc)" && \
  	make -C /usr/src/redis install && \
  	rm -r /usr/src/redis

# Install Redis 6.x
RUN set -ex && \
  	wget -O redis.tar.gz "$REDIS_6_DOWNLOAD_URL" && \
  	echo "$REDIS_6_DOWNLOAD_SHA *redis.tar.gz" | sha256sum -c - && \
  	mkdir -p /usr/src/redis6 && \
  	tar -xzf redis.tar.gz -C /usr/src/redis6 --strip-components=1 && \
  	rm redis.tar.gz && \
  	make -C /usr/src/redis6 -j "$(nproc)"

# CLEANUP
RUN set -ex && \
    apk del libgit2-dev build-base git make gcc linux-headers musl-dev cmake

# Nginx tweaks:
#
# (-) fix the nginx .pid bug (https://github.com/gliderlabs/docker-alpine/issues/185#issuecomment-246595114)
# (-) remove the default site
# (-) tweak nginx config to log errors to stderr (with increased verbosity)
# (-) tweak nginx config to redirect access logs to stdout
RUN mkdir -p /run/nginx && chown nginx:nginx /run/nginx && \
    rm /etc/nginx/conf.d/default.conf && \
    chown -R nginx:nginx /var/lib/nginx && chown -R nginx:nginx /var/log/nginx
ADD entry.html /var/lib/nginx/html/

# Redis tweaks
RUN mkdir -p /data/redis5 && chown redis:redis /data/redis5
RUN mkdir -p /data/redis6 && chown redis:redis /data/redis6
ADD nginx.conf /etc/nginx/conf.d/
ADD wait-for-it.sh /run

# Use Python 3
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1

# Supervisord tweaks
ADD supervisord.conf /etc/

# Student user and directories
RUN addgroup -S student && adduser -G student -s /bin/bash -S -h /home/student student && \
    mkdir -p /src/redisu && chown student:student /src/redisu && \
    echo 'PS1="\W$ "' >> /home/student/.bashrc
ENV HOME=/home/student
ADD .bashrc /home/student/.bashrc

# Add sanity test
ADD helloworld.py /src/redisu
RUN chown -R student:student /src/redisu

EXPOSE 8888

WORKDIR /src/redisu

CMD ["supervisord"]
