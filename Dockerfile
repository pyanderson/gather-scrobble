FROM python:3.10-slim

ENV USE_CRYPTFILE=true

RUN pip install gather-scrobble==0.1.0

ENTRYPOINT ["gather-scrobble"]
