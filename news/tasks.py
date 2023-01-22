from celery import shared_task
import time
from celery.schedules import crontab
from django.core.mail import send_mail
from django.utils.datetime_safe import date
from datetime import timedelta
from .models import Post, Category, User
from django.template.loader import render_to_string
from datetime import datetime, timedelta



@shared_task
def week_email():
    mail_list = [mail.email for mail in User.objects.all() if mail.email]
    message = ''
    for post in Post.objects.filter(time_create__gt=datetime.now() - timedelta(days=7)):
        message += f'{post.preview()}\n'
        send_mail(
            subject=f'Новости за неделю',
            message=message,
            from_email='caramba.ge@yandex.ru',
            recipient_list=mail_list
        )