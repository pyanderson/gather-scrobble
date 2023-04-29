FROM python:3.10-slim

ENV USE_CRYPTFILE=true

# RUN pip install gather-scrobble==0.0.4

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["gather-scrobble"]
