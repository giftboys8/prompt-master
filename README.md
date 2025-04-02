# 提示词管家项目

这是一个用于管理和使用提示词模板的系统。

## 项目设置

1. 克隆项目到本地。

2. 安装依赖：
   ```
   pip install -r backend/requirements/dev.txt
   ```

3. 进入后端目录：
   ```
   cd backend
   ```

4. 运行数据库迁移：
   ```
   python manage.py migrate
   ```

5. 创建超级用户：
   ```
   python manage.py createsuperuser
   ```

6. 创建默认模板：
   ```
   python manage.py create_default_templates
   ```

7. 运行开发服务器：
   ```
   python manage.py runserver
   ```

现在，您应该能够访问 http://localhost:8000/admin 并看到默认的模板已经被添加到数据库中。

## 前端设置

（在这里添加前端设置说明）

## 使用说明

（在这里添加项目的使用说明）

## 贡献指南

（在这里添加如何为项目做贡献的指南）

## 许可证

（在这里添加项目的许可证信息）