from django.contrib import admin
from django.forms import Textarea

from .models import User

admin.site.site_header = 'مدیریت پروژه'
admin.site.site_title = 'tiphub'


@admin.register(User)
class UserConfig(admin.ModelAdmin):
    model = User
    ordering = ('-start_date',)
    search_fields = ('email', 'user_name', 'first_name')

    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})}
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2',)
        }),
    )

