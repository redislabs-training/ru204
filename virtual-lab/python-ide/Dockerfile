# redislabs/python-virtual-lab
FROM redislabs/virtual-lab

RUN set -ex && \
	  apk add --no-cache py-pip && \
    pip install --upgrade pip && \
	  pip install --upgrade --no-cache-dir redis Faker
