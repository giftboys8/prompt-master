# 从 Alpine Linux 开始构建 Redis
FROM alpine:3.18

# 安装 Redis
RUN apk add --no-cache redis

# 创建 Redis 数据目录
RUN mkdir -p /data && chown redis:redis /data

# 配置 Redis 监听所有地址
RUN sed -i 's/bind 127.0.0.1 -::1/bind 0.0.0.0/g' /etc/redis.conf && \
    sed -i 's/protected-mode yes/protected-mode no/g' /etc/redis.conf && \
    sed -i 's/dir .\//dir \/data/g' /etc/redis.conf

# 切换到 redis 用户
USER redis

# 暴露端口
EXPOSE 6379

# 启动 Redis
CMD ["redis-server", "/etc/redis.conf"]