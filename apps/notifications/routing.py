from django.urls import re_path
from .consumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r"ws/posts/(?P<slug>[-a-zA-Z0-9_]+)/comments/$", CommentConsumer.as_asgi())
]