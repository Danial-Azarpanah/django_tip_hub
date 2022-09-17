from django.contrib import admin
from .models import Category, Video, Tag, Comment, UserNotification, AdminNotification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title', 'parent__title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'creator__username', 'tag__title']
    list_display = ['title', 'creator', 'show_image']
    list_filter = ['category', 'tag']
    ordering = ['-created_at']
    exclude = ['likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "show_body", "parent", "video"]
    search_fields = ["user__email", "body", "video__title"]


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ["sender", "subject"]
    search_fields = ["subject"]


admin.site.register(UserNotification)
