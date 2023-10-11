from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet


router = DefaultRouter()
app_name = 'users'

router.register(
    'users',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    # path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
