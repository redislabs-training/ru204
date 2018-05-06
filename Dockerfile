FROM gcr.io/redis-labs/virtual-lab:v2

COPY redisu/ru101 /src/redisu/ru101
COPY redisu/utils /src/redisu/utils
COPY redisu/__init__.py /src/redisu/__init__.py
COPY redisu/virtual-lab/helloworld.py /src/redisu/helloworld.py
COPY redisu/dumps/ru101.rdb /data/dump.rdb

ENV PYTHONPATH .:/src
