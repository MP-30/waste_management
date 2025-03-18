from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User  
from .models import UserProfile


admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0  
    can_delete = False  
    verbose_name_plural = 'Profile'



class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}), 
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ( 
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),  
        }),
    )
    inlines = [UserProfileInline]


admin.site.register(User, CustomUserAdmin)
