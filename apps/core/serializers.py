from django.conf import settings
from django.utils.translation import gettext_lazy as _ 


from rest_framework import serializers

from zoneinfo import available_timezones


class LanguageUpdateSerializer(serializers.Serializer):
    language = serializers.ChoiceField(
        choices=settings.LANGUAGES,
        error_messages={
            "invalid_choice": _("Unsupported language.")
        }
    )
    
    
class TimezoneUpdateSerializer(serializers.Serializer):
    timezone = serializers.CharField()
    
    def validate_timezone(self, value):
        if value not in available_timezones():
            raise serializers.ValidationError(
                _("Invalid timezone.")
            )
        return value