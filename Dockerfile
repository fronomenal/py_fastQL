FROM python:3-slim-buster

WORKDIR /usr/src/webapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV APP_DIR /usr/src/webapp
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

