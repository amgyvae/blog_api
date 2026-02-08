from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.blog.models import Category, Post, Tag, Comment

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)    

    class Meta:
        model = Comment
        fields = ["id", "author", "body", "created_at"]      
        
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)    
    category = CategorySerializer(read_only=True)    
    tags = TagSerializer(many=True, read_only=True)    
    comments = CommentSerializer(many=True, read_only=True)    
    
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "slug",
            "body",
            "category",
            "tags",
            "status",
            "created_at",
            "updated_at",
            "comments",
        ]