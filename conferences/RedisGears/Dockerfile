# redisuniversity/redisconf-2020-gears
FROM redis:6.0.1 as redis6
FROM redislabs/redisgraph:1.99.0 as redisgraph
FROM redislabs/redistimeseries:latest as redistimeseries
FROM redislabs/rejson:latest as rejson
FROM redislabs/rebloom:latest as rebloom
FROM redislabs/redisearch:1.6.10 as redisearch
FROM redislabs/redisgears:latest

# nginx
RUN set -ex && \
    apt-get install -y supervisor nginx

# Gears requirements: sqlite3, vim.
RUN set -ex && \
    apt-get install -y sqlite3 vim

# Redis Graph dependencies
RUN set -ex && \
    apt-get update && \
    apt-get install -y --no-install-recommends libgomp1

# Redis Graph, Search, TimeSeries, JSON and Bloom
ENV LIB_DEST_PATH /var/opt/redislabs/lib/modules
ENV LIB_SRC_PATH /usr/lib/redis/modules

COPY --from=redisgraph ${LIB_SRC_PATH}/redisgraph.so ${LIB_DEST_PATH}/
COPY --from=redisearch ${LIB_SRC_PATH}/redisearch.so ${LIB_DEST_PATH}/
COPY --from=redistimeseries ${LIB_SRC_PATH}/redistimeseries.so ${LIB_DEST_PATH}/
COPY --from=rejson ${LIB_SRC_PATH}/rejson.so ${LIB_DEST_PATH}/
COPY --from=rebloom ${LIB_SRC_PATH}/redisbloom.so ${LIB_DEST_PATH}/

# Redis 6
COPY --from=redis6 /usr/local/bin/redis-server /usr/local/bin/redis6-server
COPY --from=redis6 /usr/local/bin/redis-cli /usr/local/bin/redis6-cli
RUN mkdir -p /data/redis6 && chown redis:redis /data/redis6

# ttyd
RUN set -ex && \
    apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev pkg-config && \
    cd /tmp && \
    git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && \
    git checkout 1.3.3 -b 1.3.3 && \ 
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Supervisord config
ADD supervisord.conf /etc/

# nginx setup
RUN groupadd nginx && \
    useradd -g nginx -m nginx -s /bin/false && \
    mkdir -p /run/nginx && \
    chown nginx:nginx /run/nginx && \
    chown -R nginx:nginx /var/lib/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chmod 777 /run && \
    rm /etc/nginx/nginx.conf

ADD entry.html /var/lib/nginx/html/
ADD nginx.conf /etc/nginx/
ADD wait-for-it.sh /run

# Student user and directories
RUN groupadd student && \
    useradd -g student -s /bin/bash -d /home/student -m student && \
    mkdir -p /src/redisu && \
    chown student:student /src/redisu

ENV HOME=/home/student
ADD .bashrc /home/student/.bashrc

# Course files
ADD .logo /home/student/.logo

# Set permissions
RUN chown -R student:student /src/redisu
RUN chown student:student /home/student/.logo

EXPOSE 8888
WORKDIR /src/redisu

CMD ["supervisord"]