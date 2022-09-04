from django.core.validators import FileExtensionValidator
from django.utils.html import format_html
from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
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
