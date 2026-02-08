from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import RegisterViewSet

router = DefaultRouter()
router.register(r"auth/register", RegisterViewSet, basename="auth-register")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", TokenObtainPairView.as_view(), name=("token_obtain_pair")),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name=("token_refresh")),
]
