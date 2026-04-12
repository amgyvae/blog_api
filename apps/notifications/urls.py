from django.urls import path

from .views import NotificationCountView, NotificationListView, NotificationReadAllView

urlpatterns = [
    path("notifications/count/", NotificationCountView.as_view()),
    path("notifications/", NotificationListView.as_view()),
    path("notifications/read/", NotificationReadAllView.as_view()),
]
