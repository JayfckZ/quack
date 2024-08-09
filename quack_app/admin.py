from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from quack_app.models import User, Post, Comment


class MyUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
        (None, {"fields": ("handle", "password")}),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "name",
                    "email",
                    "bio",
                    "profile_pic",
                    "location",
                    "birth_date",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Relações", {"fields": ("following", "followers")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "handle",
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "profile_pic",
                    "bio",
                    "location",
                    "birth_date",
                ),
            },
        ),
    )

    list_display = ("name", "handle", "email", "is_staff")
    search_fields = ("name", "handle", "email")
    ordering = ("name",)


admin.site.register(User, MyUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
