import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@celery.task(name="create_task")
def create_task(t, string):
    time.sleep(t) # resource intensive task
    return string[::-1]
