# redisuniversity/redisconf-2020-gears
FROM redislabs/redisgraph:latest as redisgraph
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

# Redis Graph
COPY --from=redisgraph /usr/lib/redis/modules/redisgraph.so /var/opt/redislabs/lib/modules/

# ttyd
RUN set -ex && \
    apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev && \
    cd /tmp && \
    git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Supervisord config
ADD supervisord.conf /etc/

# nginx setup
RUN groupadd nginx && \
    useradd -g nginx -m nginx && \
    mkdir -p /run/nginx && \
    chown nginx:nginx /run/nginx && \
    chown -R nginx:nginx /var/lib/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
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