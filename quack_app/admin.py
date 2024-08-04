from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from quack_app.models.post import Post
from .models import User  # Ajuste conforme o nome do seu modelo

class MyUserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('handle', 'name', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('handle', 'name', 'profile_picture', 'bio', 'password1', 'password2'),
        }),
    )
    list_display = ('handle', 'name', 'is_staff')
    search_fields = ('handle', 'name')
    ordering = ('handle',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Post)