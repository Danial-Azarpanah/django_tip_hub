# Generated by Django 4.1 on 2022-09-11 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_alter_like_options_remove_like_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 11, 16, 32, 46, 480614, tzinfo=datetime.timezone.utc)),
        ),
    ]
