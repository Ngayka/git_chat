# Generated by Django 5.2.4 on 2025-07-21 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_remove_follow_created_at_alter_follow_following"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedulepost",
            name="is_post",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="chat.post",
            ),
        ),
        migrations.AlterField(
            model_name="schedulepost",
            name="schedule_time",
            field=models.DateTimeField(),
        ),
    ]
