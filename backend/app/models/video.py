from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    douyin_video_id = Column(String, unique=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    file_path = Column(String(500))
    thumbnail_path = Column(String(500))
    duration = Column(Integer)  # 视频时长(秒)
    file_size = Column(Integer)  # 文件大小(字节)
    status = Column(String(50), default="draft")  # draft, published, failed
    publish_status = Column(String(50), default="pending")  # pending, success, failed
    douyin_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="videos")
    ai_generations = relationship("AIGeneration", back_populates="video")
    publish_tasks = relationship("PublishTask", back_populates="video") 