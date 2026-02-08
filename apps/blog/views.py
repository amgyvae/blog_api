import json
import redis
from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.blog.models import Comment, Post
from apps.blog.permissions import IsAuthorOrReadOnly
from apps.blog.serializers import CommentSerializer, PostSerializer

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])

@method_decorator(cache_page(60), name="list")
class PostViewSet(viewsets.ModelViewSet):
    #queryset = Post.objects.all()
    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Post.objects.filter(status=Post.Status.PUBLISHED)
        return Post.objects.all()
    
    serializer_class = PostSerializer
    lookup_field = "slug"
    
    def get_permissions(self):
       if self.action in ["list", "retrieve"]:
           return [permissions.AllowAny()]
       return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
   
    def perform_create(self, serializer):
       serializer.save(author=self.request.user)
       
    @action(detail=True, methods=["get", "post"], serializer_class=CommentSerializer)
    def comments(self, request, slug=None):
        post = self.get_object()
        if request.method == "GET":
            serializer = CommentSerializer(post.comments.all(), many=True)
            return Response(serializer.data)
        
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.save(author=request.user, post=post)
        #return Response(serializer.data)
        comment = serializer.save(author=request.user, post=post)
        
        event = {
            "post_slug": post.slug,
            "author": str(request.user),
            "body": comment.body,
        }
        
        redis_client.publish("comments", json.dumps(event))
        
        return Response(CommentSerializer(comment).data)
