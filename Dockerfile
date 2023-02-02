FROM python:3-alpine

WORKDIR /usr/src/webapp
COPY requirements.txt .

RUN  apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
 
COPY . .

ENV APP_DIR /usr/src/webapp
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

