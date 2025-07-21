from django.urls import path, include
from rest_framework import routers

from chat.views import ProfileViewSet, FollowViewSet, PostViewSet

app_name = 'chat'

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet, basename="profiles")
router.register("follows", FollowViewSet, basename="follows")
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [path("", include(router.urls))]
