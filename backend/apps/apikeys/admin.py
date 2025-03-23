from django.contrib import admin
from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'scene_name', 'user', 'is_active', 'created_at')
    list_filter = ('platform_name', 'scene_name', 'is_active')
    search_fields = ('platform_name', 'scene_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('platform_name', 'scene_name', 'key', 'description')
        }),
        ('状态', {
            'fields': ('is_active',)
        }),
        ('用户信息', {
            'fields': ('user',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )