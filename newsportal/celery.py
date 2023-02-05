import os
from celery import Celery
from celery.schedules import crontab
import redis


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')
app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.subscribers_new_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    }}

red = redis.Redis(
    host='redis-15926.c11.us-east-1-3.ec2.cloud.redislabs.com',
    port=15926,
    password='2I7Dx8tfM7JAPRitLUa58IcgHxbqVzCO',
)

