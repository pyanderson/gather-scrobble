FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN pip install gather-scrobble==0.1.1

ENTRYPOINT ["gather-scrobble"]
