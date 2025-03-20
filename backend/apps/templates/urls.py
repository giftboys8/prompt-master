from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, TemplateVersionViewSet, TemplateTestViewSet

router = DefaultRouter()
router.register('versions', TemplateVersionViewSet, basename='template-version')
router.register('tests', TemplateTestViewSet, basename='template-test')
router.register('', TemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]