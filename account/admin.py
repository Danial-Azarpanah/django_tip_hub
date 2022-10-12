from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserEditForm

admin.site.site_header = 'مدیریت سایت'
admin.site.site_title = 'صفحه مدیریت'
admin.site.index_title = 'تیپ هاب'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserEditForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'image', 'bio',
                                     'instagram', 'github', 'linkedin', 'twitter')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'image', 'bio',
                                     'instagram', 'github', 'linkedin', 'twitter')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email', 'username', 'bio')
    ordering = ('email',)
    filter_horizontal = ()

    # Staff can only delete their own account
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.id != request.user.id:
                return False
        return True

    # Staff can only change their own account info
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is not None and obj.id != request.user.id:
                return False
        return True

    # Staff can't add new accounts
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return True

    # Field makes specified fields as read-only for staff
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return 'is_superuser', 'is_staff', 'is_active'
        return super(UserAdmin, self).get_readonly_fields(request)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
