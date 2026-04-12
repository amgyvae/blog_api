from datetime import timedelta
from celery import shared_task
from django.utils import timezone
import logging
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Comment

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_daily_stats() -> None:
    since = timezone.now() - timedelta(days=1)

    new_posts = Post.objects.filter(created_at__gte=since).count()
    new_comments = Comment.objects.filter(created_at__gte=since).count()
    new_users = User.objects.filter(date_joined__gte=since).count()

    logger.info("Daily stats: posts=%s comments=%s users=%s", new_posts, new_comments, new_users)