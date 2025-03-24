from django.contrib import admin
from .models import Framework, FrameworkModule


class FrameworkModuleInline(admin.TabularInline):
    model = FrameworkModule
    extra = 1


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    inlines = [FrameworkModuleInline]


@admin.register(FrameworkModule)
class FrameworkModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'framework', 'description', 'order', 'created_at', 'updated_at')
    list_filter = ('framework',)
    search_fields = ('name', 'description', 'framework__name')