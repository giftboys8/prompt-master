from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile
from .menu_models import Menu, UserMenu


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次输入的密码不匹配"})
        return attrs

    def validate_username(self, value):
        """
        检查用户名是否已存在
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        """
        检查邮箱是否已存在
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')  # 移除password2字段
        
        # 再次检查用户是否已存在
        username = validated_data['username']
        email = validated_data['email']
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "用户名已存在"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "邮箱已存在"})
        
        # 创建用户和用户档案
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'is_active', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'profile']
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance


class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'path', 'icon', 'parent', 'sort_order', 
                 'is_active', 'permission_code', 'children']

    def get_children(self, obj):
        if not hasattr(obj, 'children'):
            return []
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data


class UserMenuSerializer(serializers.ModelSerializer):
    menu_detail = MenuSerializer(source='menu', read_only=True)

    class Meta:
        model = UserMenu
        fields = ['id', 'user', 'menu', 'menu_detail', 'has_permission', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']