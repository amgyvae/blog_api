from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.users.serializers import RegisterSerializer

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key="ip", rate="5/m", block=True), name="create")
class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
