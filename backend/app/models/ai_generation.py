from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class AIGeneration(Base):
    __tablename__ = "ai_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    generation_type = Column(String(50))  # text, image, video
    model_name = Column(String(100))  # gpt-4, stable-diffusion, etc.
    prompt = Column(Text)
    result = Column(Text)  # 生成结果
    file_path = Column(String(500))  # 生成文件路径
    generation_metadata = Column(JSON)  # 额外元数据
    status = Column(String(50), default="pending")  # pending, success, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    video = relationship("Video", back_populates="ai_generations")
    user = relationship("User") 