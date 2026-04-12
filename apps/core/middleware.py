from django.utils import translation
from django.utils import timezone
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


import zoneinfo


class LanguageTimezoneMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        language = None
        
        if request.user.is_authenticated and hasattr(request.user, "preferred_language"):
            language = request.user.preferred_language
            
        if not language:
            language = request.GET.get("lang")
            
        if not language:
            language = request.META.get("HTTP_ACCEPT_LANGUAGE", "").split(",")[0]
            
        if not language:
            language = settings.LANGUAGE_CODE
            
        translation.activate(language)
        request.LANGUAGE_CODE = language
        

        if request.user.is_authenticated and hasattr(request.user, "timezone"):
            try:
                timezone.activate(zoneinfo.ZoneInfo(request.user.timezone))
            except Exception:
                timezone.activate("UTC")
        else:
            timezone.activate("UTC")