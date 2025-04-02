from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SceneViewSet,
    SceneTaskViewSet,
    RecommendationViewSet
)

router = DefaultRouter()
router.register(r'', SceneViewSet)  # 注册到根路径，因为外层已经有scenes前缀
router.register(r'scene-tasks', SceneTaskViewSet)
router.register(r'recommendations', RecommendationViewSet, basename='recommendations')

urlpatterns = [
    path('', include(router.urls)),
]