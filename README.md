# 抖音作品管理系统 (Douyin Manager)

## 项目简介
抖音作品管理系统是一个全栈应用，支持抖音作品的查看、AI生成内容和一键发布功能。

## 技术栈
- **后端**: FastAPI + Python 3.9+
- **前端**: Vue3 + Element Plus + Pinia
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: OAuth2.0 + JWT
- **AI生成**: OpenAI API + Stable Diffusion API

## 系统架构
```
douyin_manager/
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Vue3前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── stores/         # Pinia状态管理
│   │   ├── api/            # API调用
│   │   └── utils/          # 工具函数
│   ├── package.json
│   └── vite.config.js
├── docs/                   # 文档
└── docker-compose.yml      # Docker部署
```

## 核心功能
1. **抖音API集成**: OAuth2.0授权，获取用户作品列表
2. **AI内容生成**: 支持文本和图像生成
3. **作品管理**: 查看、编辑、删除作品
4. **一键发布**: 自动发布到抖音平台
5. **状态跟踪**: 实时监控发布状态

## 开发环境设置
```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

## API文档
启动后端服务后访问: http://localhost:8000/docs 
