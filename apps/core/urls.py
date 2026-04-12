from django.urls import path

from .views import UpdateLanguageView, UpdateTimezoneView

urlpatterns = [
    path("auth/language/", UpdateLanguageView.as_view()),
    path("auth/timezone/", UpdateTimezoneView.as_view()),
]