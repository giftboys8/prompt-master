from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import UserProfile
from .menu_models import Menu, UserMenu
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    MenuSerializer, 
    UserMenuSerializer,
    UserRegistrationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理API
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        根据不同的操作设置不同的权限
        """
        if self.action == 'create':  # 注册操作
            permission_classes = [permissions.AllowAny]
        elif self.action == 'me':  # 获取当前用户信息
            permission_classes = [IsAuthenticated]
        else:  # 其他操作需要管理员权限
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
        
    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        """
        if self.action == 'create':
            return UserRegistrationSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)
        is_active = self.request.query_params.get('is_active', None)

        if username:
            queryset = queryset.filter(username__icontains=username)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)

        return queryset

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活用户"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用用户"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        password = request.data.get('password')
        if not password:
            return Response(
                {'error': 'Password is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(password)
        user.save()
        return Response({'status': 'password reset'})


class MenuViewSet(viewsets.ModelViewSet):
    """
    菜单管理API
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Menu.objects.all()
        # 只显示顶级菜单，子菜单通过序列化器的children字段获取
        parent = self.request.query_params.get('parent', None)
        if parent == 'null':
            queryset = queryset.filter(parent__isnull=True)
        elif parent is not None:
            queryset = queryset.filter(parent=parent)
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset.order_by('sort_order')

    @action(detail=False, methods=['get'])
    def my_menus(self, request):
        """获取当前用户有权限的菜单"""
        user = request.user
        if user.is_superuser:
            # 超级管理员拥有所有菜单权限
            menus = Menu.objects.filter(parent__isnull=True, is_active=True)
        else:
            # 普通用户根据权限获取菜单
            menu_ids = UserMenu.objects.filter(
                user=user, 
                has_permission=True,
                menu__is_active=True
            ).values_list('menu_id', flat=True)
            menus = Menu.objects.filter(
                id__in=menu_ids, 
                parent__isnull=True,
                is_active=True
            )
        
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)


class UserMenuViewSet(viewsets.ModelViewSet):
    """
    用户菜单权限管理API
    """
    queryset = UserMenu.objects.all()
    serializer_class = UserMenuSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = UserMenu.objects.all()
        user_id = self.request.query_params.get('user', None)
        menu_id = self.request.query_params.get('menu', None)
        has_permission = self.request.query_params.get('has_permission', None)

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if menu_id:
            queryset = queryset.filter(menu_id=menu_id)
        if has_permission is not None:
            has_permission = has_permission.lower() == 'true'
            queryset = queryset.filter(has_permission=has_permission)
            
        return queryset

    @action(detail=False, methods=['post'])
    def batch_update(self, request):
        """批量更新用户菜单权限"""
        user_id = request.data.get('user_id')
        menu_permissions = request.data.get('menu_permissions', [])
        
        if not user_id:
            return Response(
                {'error': 'User ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        for item in menu_permissions:
            menu_id = item.get('menu_id')
            has_permission = item.get('has_permission', True)
            
            try:
                menu = Menu.objects.get(id=menu_id)
            except Menu.DoesNotExist:
                continue
                
            user_menu, created = UserMenu.objects.update_or_create(
                user=user,
                menu=menu,
                defaults={'has_permission': has_permission}
            )
            
        return Response({'status': 'permissions updated'})