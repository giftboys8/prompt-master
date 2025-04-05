from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserProfile
from .menu_models import Menu, UserMenu


class UserAPITests(APITestCase):
    def setUp(self):
        # 创建管理员用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        # 创建测试用户
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        UserProfile.objects.create(user=self.test_user)
        # 登录管理员用户
        self.client.force_authenticate(user=self.admin_user)

    def test_create_user(self):
        """测试创建用户"""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuser123',
            'profile': {
                'phone': '13800138000',
                'is_active': True
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data['username'], 'newuser')

    def test_get_user_list(self):
        """测试获取用户列表"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_user(self):
        """测试更新用户信息"""
        url = reverse('user-detail', args=[self.test_user.id])
        data = {
            'email': 'updated@example.com',
            'profile': {
                'phone': '13900139000'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'updated@example.com')

    def test_deactivate_user(self):
        """测试停用用户"""
        url = reverse('user-deactivate', args=[self.test_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertFalse(self.test_user.is_active)


class MenuAPITests(APITestCase):
    def setUp(self):
        # 创建管理员用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        # 创建测试用户
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        # 创建测试菜单
        self.parent_menu = Menu.objects.create(
            name='系统管理',
            path='/system',
            icon='setting',
            sort_order=1
        )
        self.child_menu = Menu.objects.create(
            name='用户管理',
            path='/system/users',
            icon='user',
            parent=self.parent_menu,
            sort_order=1
        )
        # 登录管理员用户
        self.client.force_authenticate(user=self.admin_user)

    def test_create_menu(self):
        """测试创建菜单"""
        url = reverse('menu-list')
        data = {
            'name': '角色管理',
            'path': '/system/roles',
            'icon': 'team',
            'parent': self.parent_menu.id,
            'sort_order': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(response.data['name'], '角色管理')

    def test_get_menu_tree(self):
        """测试获取菜单树"""
        url = reverse('menu-list')
        response = self.client.get(url, {'parent': 'null'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # 只有一个顶级菜单
        self.assertEqual(len(response.data[0]['children']), 1)  # 顶级菜单有一个子菜单

    def test_update_menu(self):
        """测试更新菜单"""
        url = reverse('menu-detail', args=[self.child_menu.id])
        data = {
            'name': '用户列表',
            'icon': 'user-list'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], '用户列表')
        self.assertEqual(response.data['icon'], 'user-list')


class UserMenuAPITests(APITestCase):
    def setUp(self):
        # 创建管理员用户
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        # 创建测试用户
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )
        # 创建测试菜单
        self.menu1 = Menu.objects.create(
            name='系统管理',
            path='/system',
            icon='setting'
        )
        self.menu2 = Menu.objects.create(
            name='用户管理',
            path='/system/users',
            icon='user',
            parent=self.menu1
        )
        # 创建用户菜单权限
        self.user_menu = UserMenu.objects.create(
            user=self.test_user,
            menu=self.menu1,
            has_permission=True
        )
        # 登录管理员用户
        self.client.force_authenticate(user=self.admin_user)

    def test_batch_update_permissions(self):
        """测试批量更新用户菜单权限"""
        url = reverse('usermenu-batch-update')
        data = {
            'user_id': self.test_user.id,
            'menu_permissions': [
                {'menu_id': self.menu1.id, 'has_permission': False},
                {'menu_id': self.menu2.id, 'has_permission': True}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证权限更新
        self.user_menu.refresh_from_db()
        self.assertFalse(self.user_menu.has_permission)
        
        new_permission = UserMenu.objects.get(
            user=self.test_user,
            menu=self.menu2
        )
        self.assertTrue(new_permission.has_permission)

    def test_get_user_menu_permissions(self):
        """测试获取用户菜单权限列表"""
        url = reverse('usermenu-list')
        response = self.client.get(url, {'user': self.test_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['menu'], self.menu1.id)
        self.assertTrue(response.data[0]['has_permission'])