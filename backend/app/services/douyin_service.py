import httpx
import json
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.user import User
from sqlalchemy.orm import Session


class DouyinService:
    """抖音API服务"""
    
    def __init__(self):
        self.base_url = settings.DOUYIN_API_BASE_URL
        self.client_id = settings.DOUYIN_CLIENT_ID
        self.client_secret = settings.DOUYIN_CLIENT_SECRET
        self.redirect_uri = settings.DOUYIN_REDIRECT_URI
    
    def get_authorization_url(self) -> str:
        """获取抖音授权URL"""
        params = {
            "client_key": self.client_id,
            "response_type": "code",
            "scope": "user_info,video.list,video.upload",
            "redirect_uri": self.redirect_uri,
            "state": "douyin_auth"
        }
        
        auth_url = f"{self.base_url}/platform/oauth/connect/"
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{auth_url}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """使用授权码换取访问令牌"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/oauth/access_token/",
                data={
                    "client_key": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"获取访问令牌失败: {response.text}")
    
    async def refresh_access_token(self, refresh_token: str) -> Dict:
        """刷新访问令牌"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/oauth/refresh_token/",
                data={
                    "client_key": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"刷新访问令牌失败: {response.text}")
    
    async def get_user_info(self, access_token: str) -> Dict:
        """获取用户信息"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/oauth/userinfo/",
                params={"access_token": access_token}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"获取用户信息失败: {response.text}")
    
    async def get_video_list(self, access_token: str, cursor: int = 0, count: int = 20) -> Dict:
        """获取用户视频列表"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/video/list/",
                params={
                    "access_token": access_token,
                    "cursor": cursor,
                    "count": count
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"获取视频列表失败: {response.text}")
    
    async def upload_video(self, access_token: str, video_file_path: str, title: str, description: str = "") -> Dict:
        """上传视频到抖音"""
        # 第一步：创建上传任务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/video/upload/",
                params={"access_token": access_token},
                data={
                    "title": title,
                    "description": description
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"创建上传任务失败: {response.text}")
            
            upload_data = response.json()
            upload_id = upload_data.get("data", {}).get("upload_id")
            
            if not upload_id:
                raise Exception("未获取到上传ID")
        
        # 第二步：上传视频文件
        with open(video_file_path, "rb") as f:
            files = {"video": f}
            response = await client.post(
                f"{self.base_url}/video/part/upload/",
                params={
                    "access_token": access_token,
                    "upload_id": upload_id,
                    "part_number": 1
                },
                files=files
            )
            
            if response.status_code != 200:
                raise Exception(f"上传视频文件失败: {response.text}")
        
        # 第三步：完成上传
        response = await client.post(
            f"{self.base_url}/video/complete/",
            params={"access_token": access_token},
            data={"upload_id": upload_id}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"完成视频上传失败: {response.text}")
    
    async def check_publish_status(self, access_token: str, task_id: str) -> Dict:
        """检查发布状态"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/video/query/",
                params={
                    "access_token": access_token,
                    "task_id": task_id
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"查询发布状态失败: {response.text}")
    
    def is_token_expired(self, expires_at: datetime) -> bool:
        """检查令牌是否过期"""
        return datetime.utcnow() >= expires_at
    
    async def ensure_valid_token(self, db: Session, user: User) -> str:
        """确保用户有有效的访问令牌"""
        if not user.douyin_access_token:
            raise Exception("用户未授权抖音账号")
        
        if self.is_token_expired(user.douyin_token_expires_at):
            # 刷新令牌
            refresh_result = await self.refresh_access_token(user.douyin_refresh_token)
            
            user.douyin_access_token = refresh_result["data"]["access_token"]
            user.douyin_refresh_token = refresh_result["data"]["refresh_token"]
            user.douyin_token_expires_at = datetime.utcnow() + timedelta(
                seconds=refresh_result["data"]["expires_in"]
            )
            
            db.commit()
        
        return user.douyin_access_token 