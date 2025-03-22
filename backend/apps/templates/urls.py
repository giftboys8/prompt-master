from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, TemplateVersionViewSet, TemplateTestViewSet

router = DefaultRouter()
router.register('versions', TemplateVersionViewSet, basename='template-version')
router.register('tests', TemplateTestViewSet, basename='template-test')
router.register('templates', TemplateViewSet, basename='template')

# 添加分享相关的路由
template_share = TemplateViewSet.as_view({
    'post': 'share',
    'delete': 'revoke_share'
})

urlpatterns = router.urls
urlpatterns += [
    path('templates/<int:pk>/share/', template_share, name='template-share'),
]