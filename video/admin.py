from django.contrib import admin

from account.models import User
from .models import Category, Video, Tag, Comment, UserNotification, AdminNotification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title', 'parent__title']

    # Staff can't create new categories
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't change a category info
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't delete a category
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['title']

    # Staff can't change Tag info
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't delete Tags
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description', 'creator__username', 'tag__title']
    list_display = ['title', 'creator', 'show_image']
    list_filter = ['category', 'tag']
    ordering = ['-created_at']
    exclude = ['likes']

    # Staff can only delete their own Video
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.creator != request.user:
                return False
        return True

    # Staff can only edit their own Video's info
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.creator != request.user:
                return False
        return True

    # Staff can only set themselves as Video creator
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "creator":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super(VideoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "show_body", "parent", "video"]
    search_fields = ["user__email", "body", "video__title"]

    # Staff can't add a comment
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't change a comment info
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't delete a comment
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ["sender", "subject"]
    search_fields = ["subject"]

    # Staff can't add site announcements
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't edit site announcements
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True

    # Staff can't delete site announcements
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return True


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):

    # No one can add user notifications
    def has_add_permission(self, request):
        return False

    # No one can edit user notifications' info
    def has_change_permission(self, request, obj=None):
        return False

    # No one can delete user notifications
    def has_delete_permission(self, request, obj=None):
        return False
