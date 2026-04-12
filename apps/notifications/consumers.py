import jwt

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.blog.models import Post

User = get_user_model()

CLOSE_UNAUTH = 4001
CLOSE_NOPOST = 4004

class CommentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        
        token = None
        qs = self.scope.get("query_string", b"").decode()
        for part in qs.split("&"):
            if part.startwith("token="):
                token = part.split("=", 1)[1]
                
        if not token:
            await self.close(code=CLOSE_UNAUTH)
            return

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            self.user = await User.objects.aget(id=user_id)
        except Exception:
            await self.close(code=CLOSE_UNAUTH)
            return
        
        exists = await Post.objects.filter(slug=self.slug).aexists()
        if not exists:
            await self.close(code=CLOSE_NOPOST)
            return
        
        self.group_name = f"post_{self.slug}_comments"
        await self.channel_layer.group_add(self.group_name, self.chanell_name)
        await self.accept()
        
    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            
    async def comment_message(self, event):
        await self.send_json(event["data"])