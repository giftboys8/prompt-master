from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FrameworkViewSet, FrameworkModuleViewSet

router = DefaultRouter()
router.register(r'admin/frameworks', FrameworkViewSet)
router.register(r'admin/modules', FrameworkModuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]