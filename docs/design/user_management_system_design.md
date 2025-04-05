# 用户管理系统设计文档

## 1. 需求概述

### 1.1 功能需求
- 管理员可以对用户进行添加、删除和权限管理
- 权限控制精确到菜单级别
- 除秘钥管理仅限管理员访问外，其他功能默认对所有用户开放

### 1.2 角色定义
- 超级管理员：系统内置角色，拥有所有权限
- 普通用户：默认角色，可访问除秘钥管理外的所有功能
- 未登录用户：无权限

## 2. 系统设计

### 2.1 数据模型设计

#### 2.1.1 扩展现有用户模型
```python
class UserProfile(models.Model):
    # 保持现有字段
    user = models.OneToOneField(User, ...)
    phone = models.CharField(...)
    avatar = models.ImageField(...)
    
    # 新增字段
    is_active = models.BooleanField(default=True)  # 用户状态
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
```

#### 2.1.2 新增菜单权限模型
```python
class Menu(models.Model):
    name = models.CharField(max_length=50)  # 菜单名称
    path = models.CharField(max_length=100)  # 菜单路径
    icon = models.CharField(max_length=50)  # 菜单图标
    sort_order = models.IntegerField(default=0)  # 排序
    is_active = models.BooleanField(default=True)  # 是否启用
    
class UserMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    has_permission = models.BooleanField(default=True)  # 是否有权限
```

### 2.2 API 设计

#### 2.2.1 用户管理接口
```
GET /api/users/  # 获取用户列表
POST /api/users/  # 创建新用户
GET /api/users/{id}/  # 获取用户详情
PUT /api/users/{id}/  # 更新用户信息
DELETE /api/users/{id}/  # 删除用户
```

#### 2.2.2 权限管理接口
```
GET /api/menus/  # 获取菜单列表
GET /api/users/{id}/menus/  # 获取用户的菜单权限
PUT /api/users/{id}/menus/  # 更新用户的菜单权限
```

### 2.3 前端界面设计

#### 2.3.1 用户管理页面
- 用户列表展示
  - 用户名
  - 邮箱
  - 手机号
  - 状态
  - 创建时间
  - 操作按钮（编辑/删除）
- 新增/编辑用户表单
  - 基本信息填写
  - 权限配置

#### 2.3.2 权限控制实现
- 前端路由守卫
- 菜单权限控制
- API 权限控制

### 2.4 安全设计
- 密码加密存储
- JWT token 认证
- API 访问权限控制
- 操作日志记录

## 3. 技术方案

### 3.1 后端实现
- Django REST framework 实现 API
- Django 内置的权限系统
- JWT 实现身份认证

### 3.2 前端实现
- Vue3 + TypeScript
- Ant Design Vue 组件库
- Vuex 状态管理
- Vue Router 路由管理

## 4. 数据迁移方案
1. 创建新的数据模型
2. 为现有用户生成默认权限配置
3. 为管理员配置全部权限

## 5. 测试方案
1. 单元测试
2. 接口测试
3. 前端组件测试
4. 集成测试
5. 用户权限测试

## 6. 部署方案
1. 数据库迁移
2. API 部署
3. 前端构建部署
4. 系统配置更新