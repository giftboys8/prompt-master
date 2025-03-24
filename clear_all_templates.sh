#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}开始清除所有提示词模板数据...${NC}"

# 1. 清除后端数据库中的模板数据
echo -e "${BLUE}步骤 1/2: 清除后端数据库中的模板数据...${NC}"
cd backend && python manage.py clear_templates
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 后端数据库模板数据已清除${NC}"
else
    echo -e "\033[0;31m✗ 后端数据库清除失败${NC}"
    exit 1
fi

# 2. 提示用户清除前端缓存
echo -e "${BLUE}步骤 2/2: 前端缓存清理${NC}"
echo -e "${GREEN}✓ 已创建缓存清理页面${NC}"
echo -e "${BLUE}请在浏览器中访问前端应用的 /clear-cache.html 页面来清除浏览器缓存${NC}"
echo -e "${GREEN}所有提示词模板数据清除完成！${NC}"