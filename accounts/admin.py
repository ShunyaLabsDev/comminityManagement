from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'mobile')
