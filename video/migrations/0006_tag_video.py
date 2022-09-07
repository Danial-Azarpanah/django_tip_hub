# Generated by Django 4.1 on 2022-09-03 07:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='images/thumbnails', verbose_name='تصویر ویدئو')),
                ('video', models.FileField(null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('length', models.TimeField()),
                ('category', models.ManyToManyField(related_name='videos', to='video.category', verbose_name='دسته بندی')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL, verbose_name='سازنده محتوا')),
                ('tag', models.ManyToManyField(related_name='videos', to='video.tag', verbose_name='تگ')),
            ],
            options={
                'verbose_name': 'ویدئو',
                'verbose_name_plural': 'ویدئوها',
            },
        ),
    ]