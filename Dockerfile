FROM gcr.io/redis-labs/virtual-lab:v9

COPY redisu/ru101/__init__.py /src/redisu/ru101/__init__.py
COPY redisu/ru101/common /src/redisu/ru101/common
COPY redisu/ru101/data /src/redisu/ru101/data
COPY redisu/ru101/uc01-faceted-search /src/redisu/ru101/uc01-faceted-search 
COPY redisu/ru101/uc02-inventory-control /src/redisu/ru101/uc02-inventory-control
COPY redisu/ru101/uc03-seat-reservation /src/redisu/ru101/uc03-seat-reservation
COPY redisu/ru101/uc05-notifications /src/redisu/ru101/uc05-notifications
COPY redisu/ru101/uc06-finding-venues /src/redisu/ru101/uc06-finding-venues

COPY redisu/utils /src/redisu/utils
COPY redisu/__init__.py /src/redisu/__init__.py
COPY redisu/virtual-lab/helloworld.py /src/redisu/helloworld.py
COPY redisu/dumps/ru101.rdb /data/dump.rdb

ENV PYTHONPATH .:/src
