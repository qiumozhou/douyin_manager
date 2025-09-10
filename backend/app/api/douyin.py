from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.video import Video
from app.models.publish_task import PublishTask
from app.api.auth import get_current_user
from app.services.douyin_service import DouyinService
from datetime import datetime

router = APIRouter()
douyin_service = DouyinService()


@router.get("/videos", response_model=dict)
async def get_douyin_videos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取抖音平台上的视频列表"""
    try:
        access_token = await douyin_service.ensure_valid_token(db, current_user)
        result = await douyin_service.get_video_list(access_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/publish/{video_id}", response_model=dict)
async def publish_video_to_douyin(video_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """将本地视频发布到抖音"""
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    try:
        access_token = await douyin_service.ensure_valid_token(db, current_user)
        result = await douyin_service.upload_video(access_token, video.file_path, video.title, video.description)
        # 创建发布任务记录
        task_id = result["data"]["task_id"]
        publish_task = PublishTask(
            video_id=video.id,
            user_id=current_user.id,
            task_id=task_id,
            status="processing",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(publish_task)
        db.commit()
        db.refresh(publish_task)
        video.publish_status = "processing"
        db.commit()
        return {"message": "发布任务已创建", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/publish/status/{task_id}", response_model=dict)
async def get_publish_status(task_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """查询抖音视频发布状态"""
    publish_task = db.query(PublishTask).filter(PublishTask.task_id == task_id, PublishTask.user_id == current_user.id).first()
    if not publish_task:
        raise HTTPException(status_code=404, detail="发布任务不存在")
    try:
        access_token = await douyin_service.ensure_valid_token(db, current_user)
        result = await douyin_service.check_publish_status(access_token, task_id)
        # 更新任务状态
        status = result["data"].get("status")
        publish_task.status = status
        publish_task.updated_at = datetime.utcnow()
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 