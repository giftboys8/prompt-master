from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    用户注册视图
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class UserInfoView(APIView):
    """
    获取当前用户信息
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义的Token获取视图，登录成功后返回用户信息
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            try:
                user = User.objects.get(username=request.data['username'])
                user_data = UserSerializer(user).data
                response.data['user'] = user_data
            except User.DoesNotExist:
                # 用户不存在时的错误处理
                pass
            
        return response