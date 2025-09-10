# 🚀 快速部署指南

## 一键启动

### Windows用户
```bash
# 构建并启动（推荐，解决构建问题）
build-and-start.bat

# 或者直接启动（如果已构建过）
start.bat
```

### Linux/Mac用户
```bash
# 给脚本添加执行权限
chmod +x *.sh

# 构建并启动（推荐，解决构建问题）
./build-and-start.sh

# 或者直接启动（如果已构建过）
./start.sh
```

## 手动启动

### 1. 配置环境变量
```bash
# 复制环境变量模板
cp docker.env .env

# 编辑配置文件（重要！）
# 配置抖音API密钥、OpenAI密钥等
nano .env
```

### 2. 启动服务
```bash
# 生产环境
docker-compose up -d

# 开发环境（支持热重载）
docker-compose -f docker-compose.dev.yml up -d
```

### 3. 访问应用
- 🌐 **前端**: http://localhost
- 🔧 **后端API**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs

## 停止服务

### Windows
```bash
stop.bat
```

### Linux/Mac
```bash
./stop.sh
```

### 手动停止
```bash
docker-compose down
```

## 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

## 故障排除

### 端口被占用
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"  # 前端改为8080端口
  - "8001:8000"  # 后端改为8001端口
```

### 权限问题
```bash
# Linux/Mac
sudo chmod -R 755 backend/uploads
```

### 查看详细日志
```bash
# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 重要配置

编辑 `.env` 文件，配置以下关键信息：

```bash
# 抖音开放平台配置
DOUYIN_CLIENT_ID=your-client-id
DOUYIN_CLIENT_SECRET=your-client-secret

# AI服务配置
OPENAI_API_KEY=your-openai-key
STABILITY_API_KEY=your-stability-key

# 安全配置
SECRET_KEY=your-super-secret-key
```

## 开发模式

开发模式支持代码热重载：

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 前端开发服务器: http://localhost:5173
# 后端开发服务器: http://localhost:8000
```

## 数据持久化

- 📁 **数据库**: `backend_db` 卷
- 📁 **上传文件**: `backend_uploads` 卷  
- 📁 **Redis数据**: `redis_data` 卷

数据在容器重启后不会丢失。

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

📖 **详细文档**: [README-Docker.md](README-Docker.md)
