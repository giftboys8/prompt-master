from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile
from .menu_models import Menu, UserMenu

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户信息'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


# 重新注册User模型
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'parent', 'sort_order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'path')
    ordering = ('sort_order',)


@admin.register(UserMenu)
class UserMenuAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'has_permission')
    list_filter = ('has_permission', 'menu')
    search_fields = ('user__username', 'menu__name')
