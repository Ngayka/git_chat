from django.contrib import admin

from chat.models import Post, Hashtag, Profile, Comment, Follow, SchedulePost

admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(SchedulePost)
