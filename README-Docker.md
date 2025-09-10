# 抖音作品管理系统 - Docker部署指南

## 项目概述

这是一个基于FastAPI + Vue 3的抖音作品管理系统，支持AI生成内容、视频管理和抖音发布功能。

## 系统架构

- **前端**: Vue 3 + Element Plus + Vite
- **后端**: FastAPI + SQLAlchemy + SQLite
- **缓存**: Redis
- **任务队列**: Celery
- **反向代理**: Nginx

## 快速开始

### 1. 环境准备

确保已安装：
- Docker
- Docker Compose

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp docker.env .env

# 编辑配置文件
vim .env
```

主要配置项：
- `SECRET_KEY`: 应用密钥
- `DOUYIN_CLIENT_ID`: 抖音开放平台客户端ID
- `DOUYIN_CLIENT_SECRET`: 抖音开放平台客户端密钥
- `OPENAI_API_KEY`: OpenAI API密钥
- `STABILITY_API_KEY`: Stability AI API密钥

### 3. 启动服务

#### 生产环境
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 开发环境
```bash
# 使用开发配置启动
docker-compose -f docker-compose.dev.yml up -d

# 查看服务状态
docker-compose -f docker-compose.dev.yml ps
```

### 4. 访问应用

- **前端应用**: http://localhost
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 服务说明

### 核心服务

1. **frontend** (端口80)
   - Vue 3前端应用
   - Nginx反向代理
   - 自动代理API请求到后端

2. **backend** (端口8000)
   - FastAPI后端服务
   - 提供RESTful API
   - 自动创建数据库表

3. **redis** (端口6379)
   - 缓存服务
   - 任务队列存储

### 可选服务

4. **celery-worker**
   - 异步任务处理
   - AI生成任务
   - 文件处理任务

5. **celery-beat**
   - 定时任务调度
   - 定期数据同步

## 数据持久化

Docker卷挂载：
- `redis_data`: Redis数据持久化
- `backend_uploads`: 上传文件存储
- `backend_db`: 数据库文件存储

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec [service_name] /bin/sh

# 重新构建镜像
docker-compose build --no-cache

# 清理未使用的资源
docker system prune -a
```

## 开发模式

开发模式支持热重载：

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 前端开发服务器 (支持热重载)
# 访问: http://localhost:5173

# 后端开发服务器 (支持热重载)
# 访问: http://localhost:8000
```

## 故障排除

### 1. 端口冲突
如果端口被占用，修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"  # 改为其他端口
```

### 2. 权限问题
```bash
# 给上传目录添加写权限
sudo chmod -R 755 backend/uploads
```

### 3. 数据库初始化
```bash
# 进入后端容器
docker-compose exec backend /bin/sh

# 手动创建表
python -c "from app.core.database import create_tables; create_tables()"
```

### 4. 查看详细日志
```bash
# 查看特定服务日志
docker-compose logs -f backend

# 查看所有服务日志
docker-compose logs -f
```

## 生产部署建议

1. **安全配置**
   - 修改默认密钥
   - 配置HTTPS
   - 设置防火墙规则

2. **性能优化**
   - 配置Redis持久化
   - 设置数据库连接池
   - 启用Gzip压缩

3. **监控告警**
   - 配置健康检查
   - 设置日志轮转
   - 监控资源使用

4. **备份策略**
   - 定期备份数据库
   - 备份上传文件
   - 配置自动备份

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

