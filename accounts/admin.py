from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': (
                'image',
                'hobi',
                'jenis_kelamin',
                'location',
                'website',
                'date_of_birth',
                'bio',
                'role',
                'theme',
                'dark_mode',
                'is_verified',
                'is_banned',
                'ban_reason',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )