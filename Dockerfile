FROM python:3.10-slim

ENV USE_CRYPTFILE=true

RUN pip install gather-scrobble==0.0.6

ENTRYPOINT ["gather-scrobble"]
