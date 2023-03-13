FROM python:3-alpine

WORKDIR /task_worker
COPY reqs.txt /task_worker

RUN python3 -m pip install -r reqs.txt --no-cache-dir

COPY . /task_worker

ENV PYTHONUNBUFFERED=1

EXPOSE 8000