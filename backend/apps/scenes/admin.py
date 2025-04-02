from django.contrib import admin
from .models import Scene, SceneTask, SceneVersion, SceneUsage


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'version', 'created_by', 'created_at', 'updated_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)


@admin.register(SceneTask)
class SceneTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'scene', 'template', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(SceneVersion)
class SceneVersionAdmin(admin.ModelAdmin):
    list_display = ('scene', 'version_number', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('scene__name', 'version_number', 'description')
    readonly_fields = ('created_at',)


@admin.register(SceneUsage)
class SceneUsageAdmin(admin.ModelAdmin):
    list_display = ('scene', 'user', 'template', 'used_at', 'feedback_score')
    list_filter = ('used_at', 'feedback_score')
    search_fields = ('scene__name', 'user__username', 'template__name')
    readonly_fields = ('used_at',)