from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, TemplateVersionViewSet, TemplateTestViewSet

router = DefaultRouter()
router.register('templates', TemplateViewSet, basename='template')
router.register('versions', TemplateVersionViewSet, basename='template-version')
router.register('tests', TemplateTestViewSet, basename='template-test')

# ViewSet 的路由已经通过 DefaultRouter 自动注册
urlpatterns = router.urls