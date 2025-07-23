from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Profile, Follow, Post, Hashtag, Comment
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
    followings = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id', 'user', "bio", "profile_pic", 'followers', 'followings')

    def get_followers(self, obj):
        followers = Follow.objects.filter(following=obj.user)
        return FollowSerializer(followers, many=True).data

    def get_followings(self, obj):
        following = Follow.objects.filter(following=obj.user)
        return FollowSerializer(following, many=True).data


class HashtagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']

class PostListSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'user', "content", "comments_count")


    def get_comments_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    hashtag = HashtagDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'user', "content", "created_at", "hashtag", "comments", "image")

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data


class SchedulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', "content", "is_post", "schedule_time")