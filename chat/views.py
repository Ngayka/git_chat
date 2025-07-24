from django.contrib.auth import get_user_model
from django.db import models

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from chat.models import Profile, Follow, Post, SchedulePost, Hashtag
from chat.paginations import StandardResultsSetPagination
from chat.permissions import IsOwnerOrReadOnly, SchedulePostPermission
from chat.serializers import (
    ProfileListSerializers,
    ProfileDetailSerializer,
    FollowSerializer,
    PostListSerializer,
    PostDetailSerializer,
    HashtagDetailSerializer,
)

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["user__username"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializers
        return ProfileDetailSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["follower__username", "following__username"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        profile = self.request.user.profile
        user = self.request.user
        follow_type = self.request.query_params.get("type")

        if follow_type == "followers":
            return Follow.objects.filter(following=user).order_by("id")
        if follow_type == "following":
            return Follow.objects.filter(follower=user).order_by("id")
        return Follow.objects.all().order_by("id")


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["user__username", "hashtag__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]


class SchedulePostViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    permission_classes = [SchedulePostPermission]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return SchedulePost.objects.filter(
                models.Q(is_post=True) & models.Q(user=user)
            )
        return SchedulePost.objects.filter(is_post=True)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagDetailSerializer
