from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _ 


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import LanguageUpdateSerializer, TimezoneUpdateSerializer


class UpdateLanguageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        serializer = LanguageUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request.user.preferred_language = serializer.validated_data("language")
        request.user.save()
        
        return Response({
            "detail": _("Language updated succesfully.")
        })
        

class UpdateTimezoneView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        serializer = TimezoneUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request.user.timezone = serializer.validated_data("timezone")
        request.user.save()
        
        return Response({
            "detail": _("Timezone updated succesfully.")
        })