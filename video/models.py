from django.core.validators import FileExtensionValidator
from django.utils.html import format_html
from django.utils.timezone import utc
from django.db import models
import datetime

from django_jalali.db import models as jmodels

from account.models import User


class Category(models.Model):
    """
    Class for nested categories
    (Every video can have multiple categories)
    """
    title = models.CharField(max_length=30, verbose_name='عنوان')
    slug = models.SlugField(allow_unicode=True, blank=True, null=True,
                            unique=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', default=None, null=True,
                               blank=True, on_delete=models.SET_NULL,
                               related_name='children',
                               verbose_name='زیردسته')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'
        ordering = ['parent__id']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Class for tags of videos
    (Every video can have multiple tags)
    """
    title = models.CharField(max_length=20, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True,
                            verbose_name='اسلاگ')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    Class for videos
    """
    title = models.CharField(max_length=50, verbose_name='عنوان')
    category = models.ManyToManyField(Category, related_name='videos',
                                      verbose_name='دسته بندی')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/thumbnails', null=True,
                              verbose_name='تصویر ویدئو')
    video = models.FileField(upload_to='videos/', null=True,
                             verbose_name='ویدئو',
                             validators=[
                                 FileExtensionValidator(
                                     allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    likes = models.ManyToManyField(User, related_name="likes", default=None, blank=True)
    like_count = models.BigIntegerField(default="0")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='videos',
                                verbose_name='سازنده محتوا')
    tag = models.ManyToManyField(Tag, related_name='videos',
                                 verbose_name='تگ')

    class Meta:
        verbose_name = 'ویدئو'
        verbose_name_plural = 'ویدئوها'
        ordering = ["-created_at"]

    # Function to show video thumbnail in admin list view
    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
        else:
            return format_html('<h3 style="color: red">بدون تصویر</h3>')

    show_image.short_description = 'تصویر'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Class for user comments on videos
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='comments', verbose_name='ویدئوی مربوطه')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='replies', null=True, blank=True,
                               verbose_name='کامنت پدر')
    body = models.TextField(verbose_name='متن کامنت')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='تاریخ و زمان')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'

    def get_time_diff(self):
        """
        Return the time difference between
        comment's submit time and now
        """
        if self.created_at:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.created_at

            if timediff.days > 365:
                return f'{timediff // 365} سال پیش'
            elif timediff.days > 30:
                return f'{timediff // 30} ماه پیش'
            elif timediff.days > 0:
                return f'{timediff.days} روز پیش'
            elif timediff.seconds > 3600:
                return f'{timediff.seconds // 3600} ساعت پیش'
            elif timediff.seconds > 60:
                return f'{timediff.seconds // 60} دقیقه پیش'
            else:
                return f'{timediff.seconds} ثانیه پیش'

    def __str__(self):
        return self.body[:20]


