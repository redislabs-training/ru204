# redisuniversity/virtual-lab-base-6
ARG ALPINE_VERSION

FROM alpine:$ALPINE_VERSION

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN addgroup -S redis && adduser -S -G redis redis

# grab su-exec for easy step-down from root
RUN apk add --no-cache 'su-exec>=0.2'

ARG REDIS_VERSION
ARG REDIS_DOWNLOAD_SHA
ARG REDIS_DOWNLOAD_URL

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

# Install Redis
RUN set -ex && \
    curl -vv $REDIS_DOWNLOAD_URL -o redis.tar.gz && \
  	echo "$REDIS_DOWNLOAD_SHA *redis.tar.gz" | sha256sum -c - && \
  	mkdir -p /usr/src/redis && \
  	tar -xzf redis.tar.gz -C /usr/src/redis --strip-components=1 && \
  	rm redis.tar.gz && \
  	make -C /usr/src/redis -j "$(nproc)" && \
    make -C /usr/src/redis install && \
    rm -r /usr/src/redis

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
RUN mkdir -p /data/redis && chown redis:redis /data/redis
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
