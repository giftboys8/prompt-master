# PromptMaster Frontend

基于 Vue 3 + TypeScript + Vite 的提示词生成与管理系统前端项目。

## 技术栈

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios

## 开发环境

### 环境要求

- Node.js 18+
- npm 7+

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 代码格式化

```bash
npm run format
```

### 代码检查

```bash
npm run lint
```

## 项目结构

```
frontend/
├── src/                    # 源代码
│   ├── api/               # API 请求
│   ├── assets/            # 静态资源
│   ├── components/        # 公共组件
│   ├── hooks/             # 自定义 hooks
│   ├── layouts/           # 布局组件
│   ├── router/            # 路由配置
│   ├── stores/            # 状态管理
│   ├── styles/            # 全局样式
│   ├── types/             # TypeScript 类型
│   ├── utils/             # 工具函数
│   └── views/             # 页面组件
├── public/                # 公共资源
├── .env                   # 环境变量
├── .env.development       # 开发环境变量
├── .env.production        # 生产环境变量
├── index.html            # HTML 模板
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript 配置
└── vite.config.ts        # Vite 配置
```

## 功能特性

- 用户认证与授权
- 业务场景管理
- 提示词模板管理
- 内容生成
- 响应式设计
- 主题定制

## API 文档

API 文档可在开发环境下访问：
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/