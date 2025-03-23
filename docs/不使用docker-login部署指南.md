# 不使用 Docker Login 的部署指南

本文档说明如何在不使用 `docker login` 的情况下部署整个应用系统。

## 原理

我们通过在本地构建所有需要的基础镜像，避免从 Docker Hub 拉取镜像，从而消除了对 Docker Login 的需求。这种方法的优点包括：

1. 无需 Docker Hub 账号
2. 适用于网络受限环境
3. 完全自主可控的构建过程
4. 可以根据需要自定义基础镜像

## 目录结构

我们添加了以下文件来支持本地构建：

```
├── backend/
│   ├── Dockerfile.python-base  # Python 基础镜像构建文件
├── frontend/
│   ├── Dockerfile.nginx-base   # Nginx 基础镜像构建文件
├── postgres/
│   ├── Dockerfile              # PostgreSQL 镜像构建文件
├── redis/
│   ├── Dockerfile              # Redis 镜像构建文件
```

## 部署步骤

### 1. 准备环境变量

复制 `.env.example` 文件到 `.env` 并根据需要修改环境变量：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置必要的环境变量。

### 2. 构建并启动服务

使用 Docker Compose 构建并启动所有服务：

```bash
docker-compose build
docker-compose up -d
```

这个过程会按照以下顺序构建和启动服务：

1. 构建基础镜像：`python-base`, `nginx-base`
2. 构建数据库服务：`postgres`, `redis`
3. 构建应用服务：`backend`, `frontend`

### 3. 验证服务状态

检查所有服务是否正常运行：

```bash
docker-compose ps
```

### 4. 访问应用

应用启动后，可以通过以下地址访问：

- 前端界面：http://localhost:3000
- 后端 API：http://localhost:8000/api/v1

## 故障排除

### 构建失败

如果某个镜像构建失败，可以单独重新构建：

```bash
docker-compose build <服务名>
```

### 服务无法启动

检查日志以获取更多信息：

```bash
docker-compose logs <服务名>
```

### 数据库连接问题

确保 PostgreSQL 服务正常运行，并且环境变量中的数据库配置正确：

```bash
docker-compose logs postgres
```

## 注意事项

1. 第一次构建可能需要较长时间，因为需要从头构建所有基础镜像
2. 确保系统有足够的磁盘空间用于构建和存储镜像
3. 如果遇到网络问题，可能需要配置合适的镜像源