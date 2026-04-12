from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.blog.models import Category, Tag, Post, Comment

class Command(BaseCommand):
    help = "Seed database with test data"

    def handle(self, *args, **options):
        User = get_user_model()

        user, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={"first_name": "Admin", "last_name": "User", "is_staff": True, "is_superuser": True},
        )
        if not user.has_usable_password():
            user.set_password("admin12345")
            user.save()

        cat, _ = Category.objects.get_or_create(slug="news", defaults={"name": "News"})
        tag, _ = Tag.objects.get_or_create(slug="django", defaults={"name": "Django"})

        post, _ = Post.objects.get_or_create(
            slug="hello",
            defaults={"author": user, "title": "Hello", "body": "Seed post", "status": Post.Status.PUBLISHED, "category": cat},
        )
        post.tags.add(tag)

        Comment.objects.get_or_create(
            post=post,
            author=user,
            body="First seed comment",
        )

        self.stdout.write(self.style.SUCCESS("Seed completed"))
        
        
        