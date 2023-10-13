from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, DisputeViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('disputes', DisputeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
