# redisuniversity/redisconf-2020-gears
FROM redislabs/redisgears:latest

# nginx
RUN set -ex && \
    apt-get install -y supervisor nginx

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

# Student user and directories
RUN groupadd student && \
    useradd -g student -s /bin/bash -d /home/student -m student && \
    mkdir -p /src/redisu && \
    chown student:student /src/redisu

# RUN addgroup -S student && adduser -G student -s /bin/bash -S -h /home/student student && \
#     mkdir -p /src/redisu && chown student:student /src/redisu && \
#     echo 'PS1="\W$ "' >> /home/student/.bashrc
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