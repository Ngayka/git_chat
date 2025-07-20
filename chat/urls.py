from django.urls import path, include
from rest_framework import routers

from chat.views import ProfileView

app_name = 'chat'

router = routers.DefaultRouter()

router.register("profiles", ProfileView)

urlpatterns = [path("", include(router.urls))]