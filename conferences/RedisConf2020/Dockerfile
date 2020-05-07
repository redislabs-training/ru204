# redisuniversity/redisconf-2020
FROM redislabs/redistimeseries:latest as redistimeseries
FROM redislabs/rejson:latest as rejson
FROM redislabs/rebloom:latest as rebloom
FROM redislabs/redisearch:1.6.10 as redisearch
#FROM redisuniversity/redisgraph-builder:latest as redisgraph
FROM redisuniversity/virtual-lab-ide6:latest

ENV LD_LIBRARY_PATH /usr/lib/redis/modules

# SQLite for Redis Gears demo
# Commented out as Gears is going to need Ubuntu...
#RUN apk add --nocache sqlite

# BEGIN GRAPH

RUN apk add --no-cache \
        build-base \
        musl-dev \
        automake \
        make \
        cmake \
        autoconf \
        libtool \
        wget \
        g++ \
        git \
        m4 \
#        libgomp \
        python \
        py-setuptools \
        py-pip \
        ;\
    pip install rmtest;\
    pip install redisgraph;

# Install PEG manually (because there is no Alpine package for it).
RUN wget https://www.piumarta.com/software/peg/peg-0.1.18.tar.gz;\
    tar xzf peg-0.1.18.tar.gz;\
    cd peg-0.1.18;\
    make; make install

# RUN rm -f /usr/lib/libgomp.a

RUN set -ex && \
    mkdir -p /usr/src/redisgraph && \
    cd /usr/src/redisgraph && \
    git clone --recurse-submodules -j8 https://github.com/RedisGraph/RedisGraph.git && \
    cd RedisGraph && \
    git checkout tags/v2.0.11 -b 2.0.11 && \
    make clean && \
    make && \
    mkdir -p ${LD_LIBRARY_PATH} && \
    cp /usr/src/redisgraph/RedisGraph/src/redisgraph.so ${LD_LIBRARY_PATH}/redisgraph.so 

# TODO cleanup...
# END GRAPH

# GEARS
#RUN set -ex && \
    # mkdir -p /usr/src/redisgears && \
    # cd /usr/src/redisgears && \
    # git clone https://github.com/RedisGears/RedisGears.git && \
    # cd RedisGears && \
    # git checkout tags/v0.99.1 -b 0.99.1 && \
    # git submodule update --init --recursive && \
    # mkdir -p /var/opt/redislabs && \
    # make setup && \
    # make fetch && \
    # make all

# END GEARS

# Install RediSearch
COPY --from=redisearch ${LD_LIBRARY_PATH}/redisearch.so ${LD_LIBRARY_PATH}/

# Install RedisTimeSeries
COPY --from=redistimeseries ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install RedisJSON
COPY --from=rejson ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install RedisBloom
COPY --from=rebloom ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

# Install RedisGraph -- COMMENTED OUT AS THIS USES THE BUILDER CONTAINER
# AND THIS VERSION SEGFAULTS...
#COPY --from=redisgraph ${LD_LIBRARY_PATH}/redisgraph.so ${LD_LIBRARY_PATH}/

# Course files
ADD .logo /home/student/.logo

# Set permissions
RUN chown -R student:student /src/redisu
RUN chown    student:student /home/student/.logo

# Supervisord config
ADD supervisord.conf /etc/