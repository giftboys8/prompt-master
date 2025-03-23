from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserInfoView, CustomTokenObtainPairView, RegisterView, UserSearchView

app_name = 'users'

urlpatterns = [
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # JWT认证
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户搜索
    path('search/', UserSearchView.as_view(), name='user_search'),
]
