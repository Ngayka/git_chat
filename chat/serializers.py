from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Profile, Follow
from user.serializers import UserSerializer, UserListSerializer

User = get_user_model()

class ProfileListSerializers(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id', 'user', "profile_pic", "followers_count", "following_count")

    def get_followers_count(self, obj):
        return obj.user.followers.count()

    def get_following_count(self, obj):
        return obj.user.following.count()

class FollowSerializer(serializers.ModelSerializer):
    follower = UserListSerializer(read_only=True)
    following = UserListSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id', 'user', "bio", "profile_pic")

    def get_followers(self, obj):
        followers = Follow.objects.filter(following__user=obj)
        return FollowSerializer(followers, many=True).data

    def get_follow(self, obj):
        following = Follow.objects.filter(following__user=obj)
        return FollowSerializer(following, many=True).data



