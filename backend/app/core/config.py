from pydantic_settings import BaseSettings
from typing import Optional, List, Union
import os
import json


class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "抖音作品管理系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./douyin_manager.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # 抖音API配置
    DOUYIN_CLIENT_ID: Optional[str] = None
    DOUYIN_CLIENT_SECRET: Optional[str] = None
    DOUYIN_REDIRECT_URI: str = "http://localhost:3000/auth/callback"
    DOUYIN_API_BASE_URL: str = "https://open.douyin.com"
    
    # AI生成配置
    OPENAI_API_KEY: Optional[str] = None
    STABILITY_API_KEY: Optional[str] = None
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # CORS配置
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001"
    ]
    
    @property
    def cors_origins(self) -> List[str]:
        """处理CORS origins，支持字符串和列表格式"""
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            try:
                # 尝试解析JSON字符串
                return json.loads(self.BACKEND_CORS_ORIGINS)
            except json.JSONDecodeError:
                # 如果不是JSON，按逗号分割
                return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]
        return self.BACKEND_CORS_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 