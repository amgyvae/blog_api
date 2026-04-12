import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.env.local")

app = Celery("blog")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "publish_scheduled_posts_every_minute": {
        "task": "apps.blog.tasks.publish_scheduled_posts",
        "schedule": 60.0,
    },
    "clear_expired_notifications_daily": {
        "task": "apps.notifications.tasks.clear_expired_notifications",
        "schedule": crontab(hour=3, minute=0),
    },
    "generate_daily_stats_daily": {
        "task": "apps.core.tasks.generate_daily_stats",
        "schedule": crontab(hour=0, minute=0),
    },
}