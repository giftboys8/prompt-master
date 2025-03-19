from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """用户注册视图"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """用户登录视图"""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return Response({
                    'user': UserSerializer(user).data,
                    'message': '登录成功'
                })
            else:
                return Response({
                    'message': '用户名或密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """用户登出视图"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'message': '登出成功'})

class UserProfileView(generics.RetrieveUpdateAPIView):
    """用户资料视图"""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """获取当前用户信息"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)