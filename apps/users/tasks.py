from celery import shared_task

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation

User = get_user_model()

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_welcome_email_task(user_id: int) -> None:
    user = User.objects.get(id=user_id)

    current_lang = translation.get_language()
    translation.activate(user.user_language)

    subject = render_to_string("emails/welcome/subject.txt", {"user": user}).strip()
    body = render_to_string("emails/welcome/body.txt", {"user": user})

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

    translation.activate(current_lang)