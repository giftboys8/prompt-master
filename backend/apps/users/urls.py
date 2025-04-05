from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .auth import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'user-menus', views.UserMenuViewSet)

urlpatterns = [
    # JWT认证相关路由
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户管理相关路由
    path('', include(router.urls)),
]