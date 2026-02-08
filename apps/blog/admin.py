from django.contrib import admin

from apps.blog.models import Category, Tag, Comment, Post

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Post)

