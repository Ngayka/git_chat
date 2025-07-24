from django.utils import timezone
from django.utils.timezone import now

from celery import shared_task

from chat.models import Post


@shared_task
def publish_posts():
    now_time = timezone.now()
    posts = Post.objects.filter(schedule_time__lte=now_time, is_posted=False)
    for scheduled in posts:
        Post.user.create(user=scheduled.user, content=scheduled.content)
        scheduled.is_posted = True
        scheduled.save()
