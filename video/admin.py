from django.contrib import admin
from .models import Category, Video, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title', 'parent__title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'creator', 'tag']
    list_display = ['title', 'creator', 'show_image']
    list_filter = ['category', 'tag']
    ordering = ['-created_at']
