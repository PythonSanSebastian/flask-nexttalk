FROM balenalib/rpi-alpine:3.10

ENV TZ 'Europe/Berlin'

ENV SICKRAGE_VERSION 9.4.132

RUN apk add --update --no-cache libffi-dev openssl-dev libxml2-dev libxslt-dev linux-headers build-base \
    git tzdata unrar \
    python3 python3-dev
RUN git clone https://github.com/SiCKRAGE/SiCKRAGE.git -b ${SICKRAGE_VERSION} --depth 1 /opt/sickrage \
    && cd /opt/sickrage; git checkout ${SICKRAGE_VERSION} \
    && python3 -m pip install -U pip setuptools \
    && python3 -m pip install -r /opt/sickrage/requirements.txt

## Expose port
EXPOSE 8081

## Run
ENTRYPOINT ["python3", "/opt/sickrage/SiCKRAGE.py", "--datadir=/config"]
