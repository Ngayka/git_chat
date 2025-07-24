import self
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status

from chat.models import Post, Profile, Follow
from chat.serializers import PostDetailSerializer, ProfileListSerializers, FollowSerializer

User = get_user_model()
class PostViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user1",
            email="test@gmail.com",
            password="testpassword123"
        )
    self.client.force_authenticate(user=self.user)
    def test_post_detail_view(self):
        post = Post.objects.create(
            user=self.user,
            content="It`s test content")

        url = reverse("chat: post-detail", args=[post.id])
        res = self.client.get(url)
        serializer = PostDetailSerializer(post)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="user1",
            email="user1@test.com",
            password="user123"
        )
        self.user2 = User.objects.create(
            username="user2",
            email="user2@test.com",
            password="user456"
        )
        self.profile1 = Profile.objects.create(user=self.user1, bio="bio 1")
        self.profile2 = Profile.objects.create(user=self.user2, bio="bio 2")

        self.client.force_authenticated(user=self.user1)

    def test_filter_by_username(self):
        url = reverse("api/chat/profiles")
        response = self.client.get(url, {"user__username": "user1"})
        expected_data = ProfileListSerializers([self.profile1], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"]["username"], "user1")

class FollowViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="user1",
            email="user1@test.com",
            password="user123"
        )
        self.user2 = User.objects.create(
            username="user2",
            email="user2@test.com",
            password="user456"
        )
        self.user3 = User.objects.create(
            username="user3",
            email="user3@test.com",
            password="user789"
        )
        Follow.objects.create(follower=self.user1, following=self.user1)
        Follow.objects.create(follower=self.user3, following=self.user1)
        Follow.objects.create(follower=self.user1, following=self.user3)

        self.client.force_authenticated(user=self.user1)

    def test_followers_type(self):
        url = reverse("api/chat/follows") + "?type=following"
        response = self.client.get(url)
        expected = Follow.objects.filter(following=self.user1)
        serialized= FollowSerializer(expected, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], serialized.data)
        self.assertEqual(len(response.data), 2)

    def test_all_follows(self):
        url = reverse("api/chat/follows")
        response = self.client.get(url)
        expected = Follow.objects.all()
        serialized = FollowSerializer(expected, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], serialized.data)
        self.assertEqual(len(response.data), 3)
