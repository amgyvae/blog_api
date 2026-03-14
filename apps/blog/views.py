import json
import redis

from django.conf import settings
from django.core.cache import cache
from django.utils import translation

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from apps.blog.models import Post
from apps.blog.serializers import PostSerializer, CommentSerializer
from apps.blog.permissions import IsAuthorOrReadOnly


redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"

    filterset_fields = ["category"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Post.objects.filter(status=Post.Status.PUBLISHED)
        return Post.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "comments"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]

    def invalidate_posts_cache(self):
        for lang_code, _ in settings.LANGUAGES:
            cache.delete(f"posts_list_{lang_code}")

    @extend_schema(
        summary="List all published posts",
        description=(
            "Returns paginated list of published posts. "
            "Response is cached in Redis per language. "
            "Cache is invalidated whenever a post is created, updated, or deleted. "
            "Dates are formatted according to user's timezone."
        ),
        tags=["Posts"],
        responses={
            200: PostSerializer(many=True),
            429: OpenApiResponse(description="Too many requests"),
        },
    )
    def list(self, request, *args, **kwargs):
        language = translation.get_language()
        cache_key = f"posts_list_{language}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60)
        return response

    @extend_schema(
        summary="Create a new post",
        description=(
            "Creates a new post. "
            "Authentication required. "
            "Invalidates Redis cache for all languages."
        ),
        tags=["Posts"],
        responses={
            201: PostSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
        examples=[
            OpenApiExample(
                "Create Post Example",
                value={
                    "title": "My First Post",
                    "content": "This is a post.",
                    "status": "published"
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        self.invalidate_posts_cache()

    @extend_schema(
        summary="Update a post",
        description=(
            "Updates a post. "
            "Only author can modify. "
            "Invalidates Redis cache for all languages."
        ),
        tags=["Posts"],
        responses={
            200: PostSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_posts_cache()

    @extend_schema(
        summary="Delete a post",
        description=(
            "Deletes a post. "
            "Only author can delete. "
            "Invalidates Redis cache for all languages."
        ),
        tags=["Posts"],
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
        self.invalidate_posts_cache()

    @extend_schema(
        summary="Get or create comments for a post",
        description=(
            "GET returns all comments for the post. "
            "POST creates a new comment and publishes a Redis event."
        ),
        tags=["Comments"],
        responses={
            200: CommentSerializer(many=True),
            201: CommentSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    @action(detail=True, methods=["get", "post"], serializer_class=CommentSerializer)
    def comments(self, request, slug=None):
        post = self.get_object()

        if request.method == "GET":
            serializer = CommentSerializer(post.comments.all(), many=True)
            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save(
            author=request.user,
            post=post,
        )

        event = {
            "post_slug": post.slug,
            "author_id": request.user.id,
            "body": comment.body,
        }

        redis_client.publish("comments", json.dumps(event))

        return Response(CommentSerializer(comment).data, status=201)