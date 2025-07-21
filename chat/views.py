from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from chat.models import Profile, Follow, Post
from chat.paginations import StandardResultsSetPagination
from chat.permissions import IsOwnerOrReadOnly
from chat.serializers import (
    ProfileListSerializers,
    ProfileDetailSerializer,
    FollowSerializer,
    PostListSerializer,
    PostDetailSerializer,
)

User = get_user_model()

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializers
        return ProfileDetailSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        return Follow.objects.filter(following__user=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
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
