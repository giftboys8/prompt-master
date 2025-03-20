from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserInfoView, CustomTokenObtainPairView

app_name = 'users'

urlpatterns = [
    # JWT认证
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 用户信息
    path('user/', UserInfoView.as_view(), name='user_info'),
]