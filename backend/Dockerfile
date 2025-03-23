# 使用本地构建的Python基础镜像
FROM python-base:latest

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

# 复制入口点脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 复制项目代码
COPY . .

# 创建静态文件和媒体文件目录
RUN mkdir -p /app/staticfiles /app/mediafiles

# 暴露端口
EXPOSE 8000

# 设置入口点
ENTRYPOINT ["/entrypoint.sh"]

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]