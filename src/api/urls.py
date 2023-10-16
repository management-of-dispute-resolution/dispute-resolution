from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (  # CommentDetailViewSet,
    CommentViewSet,
    CustomUserViewSet,
    DisputeViewSet,
)

app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('disputes', DisputeViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    # path(
    #     'api/comments/<int:pk>/',
    #     CommentDetailViewSet.as_view(),
    #     name='comment-detail',
    # ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
