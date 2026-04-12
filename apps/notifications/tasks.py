import json

from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.blog.models import Comment
from apps.notifications.models import Notification

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_new_comment_task(comment_id: int) -> None:
    comment = Comment.objects.select_related("post", "author").get(id=comment_id)
    post = comment.post
    recipient = post.author

    if comment.author_id != recipient.id:
        Notification.objects.create(recipient=recipient, comment=comment)

    payload = {
        "comment_id": comment.id,
        "author": {"id": comment.author_id, "email": comment.author.email},
        "body": comment.body,
        "created_at": comment.created_at.isoformat(),
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"post_{post.slug}_comments",
        {"type": "comment_message", "data": payload},
    )

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def clear_expired_notifications() -> None:
    cutoff = timezone.now() - timedelta(days=30)
    Notification.objects.filter(created_at__lt=cutoff).delete()