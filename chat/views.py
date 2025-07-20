from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions

from chat.models import Profile
from chat.permissions import IsOwnerOrReadOnly
from chat.serializers import ProfileListSerializers, ProfileDetailSerializer

User = get_user_model()

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializers
        return ProfileDetailSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
