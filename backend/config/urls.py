from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="PromptMaster API",
        default_version='v1',
        description="提示词管理系统API文档",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API 文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API 路由
    path('api/v1/', include([
        path('auth/', include('apps.users.urls', namespace='auth')),  # 用户认证相关接口
        path('users/', include('apps.users.urls', namespace='users')),  # 添加用户相关接口
        path('scenes/', include('apps.scenes.urls')),
        path('templates/', include('apps.templates.urls')),
        path('contents/', include('apps.contents.urls')),
        path('', include('apps.apikeys.urls')),
    ])),
]