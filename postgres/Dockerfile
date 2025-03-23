# 从 Alpine Linux 开始构建 PostgreSQL
FROM alpine:3.18

# 安装 PostgreSQL
RUN apk add --no-cache postgresql16 postgresql16-contrib

# 设置环境变量
ENV PGDATA=/var/lib/postgresql/data

# 创建数据目录
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 700 "$PGDATA"

# 切换到 postgres 用户
USER postgres

# 初始化数据库
RUN initdb -D "$PGDATA"

# 配置 PostgreSQL 监听所有地址
RUN echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf" && \
    echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"

# 暴露端口
EXPOSE 5432

# 启动 PostgreSQL
CMD ["postgres", "-D", "/var/lib/postgresql/data"]