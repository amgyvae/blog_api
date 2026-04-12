from django.contrib.auth import get_user_model
from django.utils import formats
from django.utils.timezone import localtime
from django.utils import translation


from rest_framework import serializers


from apps.blog.models import Category, Post, Tag, Comment


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        
    def get_name(self, obj):
        lang = translation.get_language()

        if lang == "ru":
            return obj.name_ru
        elif lang == "kk":
            return obj.name_kk
        else:
            return obj.name_en
        
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
    
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()  
    
    def get_created_at(self, obj):
        dt = localtime(obj.created_at)
        return formats.date_format(dt, "DATETIME_FORMAT")
    
    def get_updated_at(self, obj):
        dt = localtime(obj.updated_at)
        return formats.date_format(dt, "DATETIME_FORMAT")
        
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