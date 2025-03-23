#!/bin/sh

# 等待PostgreSQL启动
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# 等待Redis启动
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis started"

# 执行数据库迁移
echo "Applying database migrations..."
python manage.py migrate

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 启动应用
echo "Starting application..."
exec "$@"