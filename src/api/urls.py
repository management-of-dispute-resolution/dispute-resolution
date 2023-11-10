from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, CustomUserViewSet, DisputeViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('disputes', DisputeViewSet, basename='disputes')
router.register(
    r'disputes/(?P<dispute_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
