from fastapi import APIRouter
from .auth import router as auth_router
from .videos import router as videos_router
from .ai import router as ai_router
from .douyin import router as douyin_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(videos_router, prefix="/videos", tags=["视频管理"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI生成"])
api_router.include_router(douyin_router, prefix="/douyin", tags=["抖音集成"]) 