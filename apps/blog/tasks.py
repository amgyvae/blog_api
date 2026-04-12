import json
import redis

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from apps.blog.models import Post

redis_client = redis.Redis.from_url(settings.BLOG_REDIS_URL)

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def invalidate_posts_cache_task() -> None:
    for lang_code, _ in settings.LANGUAGES:
        cache.delete(f"posts_list_{lang_code}")

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def publish_scheduled_posts() -> None:
    now = timezone.now()
    posts = Post.objects.select_related("author").filter(
        status=Post.Status.SCHEDULED,
        publish_at__isnull=False,
        publish_at__lte=now,
    )

    for post in posts:
        post.status = Post.Status.PUBLISHED
        post.save(update_fields=["status"])

        event = {
            "post_id": post.id,
            "title": post.title,
            "slug": post.slug,
            "author": {"id": post.author_id, "email": post.author.email},
            "published_at": timezone.now().isoformat(),
        }
        redis_client.publish("posts_published", json.dumps(event))