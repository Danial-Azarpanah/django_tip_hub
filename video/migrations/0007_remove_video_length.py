# Generated by Django 4.1 on 2022-09-03 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_tag_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='length',
        ),
    ]
