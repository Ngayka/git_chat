from django.urls import path, include
from rest_framework import routers

from chat.permissions import SchedulePostPermission
from chat.views import (
    ProfileViewSet,
    FollowViewSet,
    PostViewSet,
    SchedulePostViewSet,
    HashtagViewSet,
)

app_name = 'chat'

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet, basename="profiles")
router.register("follows", FollowViewSet, basename="follows")
router.register("posts", PostViewSet, basename="posts")
router.register("hashtags", HashtagViewSet, basename="hashtags")
router.register("schedule_posts", SchedulePostViewSet, basename="schedule_posts")

urlpatterns = [path("", include(router.urls))]
