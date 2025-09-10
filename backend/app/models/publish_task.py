from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class PublishTask(Base):
    __tablename__ = "publish_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(String, unique=True, index=True)  # 抖音任务ID
    status = Column(String(50), default="pending")  # pending, processing, success, failed
    progress = Column(Integer, default=0)  # 进度百分比
    error_message = Column(Text)
    douyin_video_id = Column(String)  # 发布后的抖音视频ID
    douyin_url = Column(String(500))  # 发布后的抖音链接
    task_metadata = Column(JSON)  # 发布相关元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    video = relationship("Video", back_populates="publish_tasks")
    user = relationship("User") 