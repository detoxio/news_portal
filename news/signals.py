from datetime import timedelta

from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed


from .models import Post, Category


@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    send_mail(
        subject=f'Dear {email_address.user} Welcome to News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='defferius@yandex.ru',
        recipient_list=[email_address.user.email]
    )


@receiver(m2m_changed, sender=Post.categories.through)
def new_post(sender, action, instance, **kwargs):
    if action == 'post_add':
        for each in instance.categories.all():
            for cat in each.subscribers.all():
                send_mail(
                    subject=f'Выложен новый пост "{instance.headline}"!',
                    message=f'Привет, {cat}! На новостном портале новый пост по твоей подписке'
                            f' - "{instance.content[:30]}", '
                            f'переходи по ссылке - http://127.0.0.1:8000/news/{instance.id}',
                    from_email='defferius@yandex.ru',
                    recipient_list=[cat.email]
                )