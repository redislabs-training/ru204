# redisuniversity/virtual-lab-base
FROM redisai/redisai

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN adduser --system --group redis

ARG REDIS_VERSION
ARG REDIS_DOWNLOAD_SHA
ARG REDIS_DOWNLOAD_URL


# Nginx tweaks:
#
# (-) fix the nginx .pid bug (https://github.com/gliderlabs/docker-alpine/issues/185#issuecomment-246595114)
# (-) remove the default site
# (-) tweak nginx config to log errors to stderr (with increased verbosity)
# (-) tweak nginx config to redirect access logs to stdout
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nginx-light \
                                                      apt-utils \
                                                      python \
                                                      python-pip \
												      curl \
												      git \
												      vim \
												      zip \
												      python \
												      python-pip \
												      dpkg \
												      supervisor \
												      wget \
												      curl && \
# TTYD
    DEBIAN_FRONTEND=noninteractive apt-get install -y cmake \
    												  g++ \
    												  pkg-config \
    												  git \
    												  vim-common \
    												  libwebsockets-dev \
    												  libjson-c-dev \
    												  libssl-dev && \
    git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && mkdir build && cd build && \
    cmake .. && \
    make -j8 && make install && \
    DEBIAN_FRONTEND=noninteractive apt-get remove -y \
    									   cmake \
    									   make \
    									   g++ \
    									   pkg-config \
    									   git \
    									   libwebsockets-dev \
    									   libjson-c-dev \
    									   libssl-dev && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
    									   g++ \
    									   make \
    									   libgit2-dev && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs && \
# INSTALL `ORION` USING `NPM`
#
# Parameters:
#
# (-) BUILD_ONLY=true: https://github.com/nodegit/nodegit/issues/1039#issuecomment-223516656
# (-) --production:    https://wiki.eclipse.org/Orion/Node/Getting_started#Installing_with_npm
# (-) --unsafe-perm:   https://github.com/nodejs/node-gyp/issues/454#issuecomment-134140378
    BUILD_ONLY=true npm install --production --unsafe-perm -g orion && \
    rm -rf /tmp/* /var/cache/apk/* && \
# CLEANUP
    DEBIAN_FRONTEND=noninteractive apt-get remove -y libgit2-dev g++ make && \
# Python 3.6
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      									   make \
      									   build-essential \
      									   libssl-dev \
      									   zlib1g-dev \
      									   libbz2-dev \
      									   libreadline-dev \
      									   libsqlite3-dev \
      									   wget \
      									   curl \
      									   llvm \
      									   libncurses5-dev \
      									   libncursesw5-dev \
      									   xz-utils \
      									   tk-dev \
      									   libffi-dev \
      									   liblzma-dev && \
    wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz && \
    tar xvf Python-3.6.3.tgz && \
    cd Python-3.6.3 && \
    ./configure --with-ensurepip=install && \
    make -j8 && \
    make install && \
    cd .. && \
    rm -rf Python-3.6.3 && \
    DEBIAN_FRONTEND=noninteractive apt-get remove -y make \
                                           build-essential \
                                           libssl-dev \
                                           zlib1g-dev \
                                           libbz2-dev \
        								   libreadline-dev \
        								   libsqlite3-dev \
        								   llvm \
        								   libncurses5-dev \
        								   libncursesw5-dev \
        								   xz-utils \
        								   tk-dev \
        								   libffi-dev \
        								   liblzma-dev && \
# Redis Python
	pip3 install --upgrade --no-cache-dir redis==3.0.1 

# Nginx tweaks:
ADD entry.html /var/lib/nginx/html/
ADD nginx.conf /etc/nginx/conf.d/

# NGINX tweaks
# Nginx tweaks:
#
# (-) fix the nginx .pid bug (https://github.com/gliderlabs/docker-alpine/issues/185#issuecomment-246595114)
# (-) remove the default site
# (-) tweak nginx config to log errors to stderr (with increased verbosity)
# (-) tweak nginx config to redirect access logs to stdout
ADD entry.html /var/lib/nginx/html/
RUN addgroup --system nginx && adduser --system --no-create-home --ingroup nginx nginx && \
    mkdir -p /run/nginx && chown nginx:nginx /run/nginx && \
#    rm /etc/nginx/conf.d/default.conf && \
    sed -i 's:/var/log/nginx/error.log warn:stderr notice:g' /etc/nginx/nginx.conf && \
    chown -R nginx:nginx /var/lib/nginx && chown -R nginx:nginx /var/log/nginx

# Redis tweaks
#RUN mkdir /data && chown redis:redis /data
ADD nginx.conf /etc/nginx/conf.d/
ADD wait-for-it.sh /run

# Use Python 3
# RUN pip3 install --upgrade --no-cache-dir redis==3.0.1 

# Supervisord tweaks
ADD supervisord.conf /etc/

# Student user and directories
RUN addgroup --system student && adduser --system --ingroup student --shell /bin/bash  student && \
    mkdir -p /src/redisu && chown student:student /src/redisu && \
    echo 'PS1="\W$ "' >> /home/student/.bashrc
ENV HOME=/home/student
ADD .bashrc /home/student/.bashrc
ADD .logo /home/student/.logo

# Add sanity test
ADD helloworld.py /src/redisu
RUN chown -R student:student /src/redisu

EXPOSE 8888

WORKDIR /src/redisu

CMD ["supervisord"]
