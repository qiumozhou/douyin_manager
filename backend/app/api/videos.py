from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.video import Video
from app.models.user import User
from app.api.auth import get_current_user
from datetime import datetime
import os

router = APIRouter()


@router.get("/", response_model=List[dict])
async def list_videos(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取当前用户的视频列表"""
    videos = db.query(Video).filter(Video.user_id == current_user.id).offset(skip).limit(limit).all()
    return [
        {
            "id": v.id,
            "title": v.title,
            "description": v.description,
            "status": v.status,
            "publish_status": v.publish_status,
            "douyin_url": v.douyin_url,
            "created_at": v.created_at,
            "updated_at": v.updated_at
        } for v in videos
    ]


@router.post("/upload", response_model=dict)
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传视频文件"""
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    video = Video(
        user_id=current_user.id,
        title=title,
        description=description,
        file_path=file_path,
        status="draft",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"id": video.id, "title": video.title, "file_path": video.file_path}


@router.get("/{video_id}", response_model=dict)
async def get_video(video_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取单个视频详情"""
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "status": video.status,
        "publish_status": video.publish_status,
        "douyin_url": video.douyin_url,
        "created_at": video.created_at,
        "updated_at": video.updated_at
    }


@router.put("/{video_id}", response_model=dict)
async def update_video(video_id: int, title: Optional[str] = Form(None), description: Optional[str] = Form(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """更新视频信息"""
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    if title:
        video.title = title
    if description:
        video.description = description
    video.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(video)
    return {"id": video.id, "title": video.title, "description": video.description}


@router.delete("/{video_id}", response_model=dict)
async def delete_video(video_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """删除视频"""
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    db.delete(video)
    db.commit()
    return {"message": "删除成功"} 