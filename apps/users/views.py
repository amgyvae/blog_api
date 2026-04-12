from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.users.serializers import RegisterSerializer
from apps.users.tasks import send_welcome_email_task

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import translation
from django.conf import settings

@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="create")
class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        send_welcome_email_task.delay(user.id)
        
        '''data = serializer.save()'''
        return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                , status=status.HTTP_201_CREATED
            )
    '''
    def send_welcome_email(user):
        current_language = translation.get_language()
        translation.activate(user.user_language)
        
        subject = render_to_string("emails/welcome/subject.txt", {"user": user}).strip()
        message = render_to_string("emails/welcome/body.txt", {"user": user})
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        
        translation.activate(current_language)
    '''