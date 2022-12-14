# Generated by Django 4.1 on 2022-09-19 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0027_video_like_count_video_likes_delete_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ادرس آی پی')),
            ],
            options={
                'verbose_name': 'آدرس آی پی',
                'verbose_name_plural': 'آدرس\u200cهای آی پی',
            },
        ),
    ]
