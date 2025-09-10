from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.post("/text", response_model=dict)
async def generate_text(prompt: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """AI生成文本内容"""
    result = await ai_service.generate_text(prompt)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/title", response_model=dict)
async def generate_title(content: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """AI生成视频标题"""
    result = await ai_service.generate_video_title(content)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/description", response_model=dict)
async def generate_description(title: str, content: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """AI生成视频描述"""
    result = await ai_service.generate_video_description(title, content)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/image", response_model=dict)
async def generate_image(prompt: str, model: str = "stable-diffusion", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """AI生成图片"""
    result = await ai_service.generate_image(prompt, model=model)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result 