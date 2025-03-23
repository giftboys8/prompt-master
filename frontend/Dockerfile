# 构建阶段 - 使用 debian slim 作为基础
FROM debian:bullseye-slim AS build-stage

# 安装 Node.js 和 npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制项目文件
COPY . .

# 构建项目
RUN npm run build

# 生产阶段 - 使用本地构建的 Nginx 基础镜像
FROM nginx-base:latest AS production-stage

# 复制构建文件到Nginx服务目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 删除默认的nginx配置
RUN rm -f /etc/nginx/sites-enabled/default