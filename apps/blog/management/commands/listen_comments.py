import json
import redis
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Listen for new comment events from Redis"
    
    def handle(self, *args, **options):
        client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])
        pubsub = client.pubsub()
        pubsub.subscribe("comments")
        
        self.stdout.write(self.style.SUCCESS("Listening for comment events..."))
        
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                self.stdout.write(f"New comment: {data}")