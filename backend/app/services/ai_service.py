import openai
import httpx
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from app.core.config import settings
from PIL import Image
import io


class AIService:
    """AI生成服务"""
    
    def __init__(self):
        # 只有在有API密钥时才初始化客户端
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
        self.stability_api_key = settings.STABILITY_API_KEY
    
    async def generate_text(self, prompt: str, model: str = "gpt-4", max_tokens: int = 500) -> Dict:
        """生成文本内容"""
        if not self.openai_client:
            return {
                "success": False,
                "error": "OpenAI API密钥未配置"
            }
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的短视频内容创作者，擅长创作吸引人的视频标题和描述。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return {
                "success": True,
                "result": response.choices[0].message.content,
                "model": model,
                "usage": response.usage.dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_image(self, prompt: str, model: str = "stable-diffusion", size: str = "1024x1024") -> Dict:
        """生成图像内容"""
        if model == "stable-diffusion":
            return await self._generate_stable_diffusion_image(prompt, size)
        elif model == "dall-e":
            return await self._generate_dalle_image(prompt, size)
        else:
            return {"success": False, "error": f"不支持的模型: {model}"}
    
    async def _generate_stable_diffusion_image(self, prompt: str, size: str) -> Dict:
        """使用Stable Diffusion生成图像"""
        if not self.stability_api_key:
            return {
                "success": False,
                "error": "Stability API密钥未配置"
            }
        
        try:
            # 这里使用Stability AI的API
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.stability_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    # 保存图像文件
                    image_data = result["artifacts"][0]["base64"]
                    image_bytes = bytes(image_data, "utf-8")
                    
                    # 生成文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ai_generated_{timestamp}.png"
                    file_path = os.path.join(settings.UPLOAD_DIR, filename)
                    
                    # 保存图像
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                    
                    return {
                        "success": True,
                        "result": "图像生成成功",
                        "file_path": file_path,
                        "model": "stable-diffusion",
                        "prompt": prompt
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Stable Diffusion API错误: {response.text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_dalle_image(self, prompt: str, size: str) -> Dict:
        """使用DALL-E生成图像"""
        if not self.openai_client:
            return {
                "success": False,
                "error": "OpenAI API密钥未配置"
            }
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            # 下载图像
            image_url = response.data[0].url
            async with httpx.AsyncClient() as client:
                image_response = await client.get(image_url)
                
                if image_response.status_code == 200:
                    # 生成文件名
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ai_generated_{timestamp}.png"
                    file_path = os.path.join(settings.UPLOAD_DIR, filename)
                    
                    # 保存图像
                    with open(file_path, "wb") as f:
                        f.write(image_response.content)
                    
                    return {
                        "success": True,
                        "result": "图像生成成功",
                        "file_path": file_path,
                        "model": "dall-e",
                        "prompt": prompt
                    }
                else:
                    return {
                        "success": False,
                        "error": "下载生成的图像失败"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_video_script(self, topic: str, duration: int = 60) -> Dict:
        """生成视频脚本"""
        prompt = f"""
        请为以下主题创作一个{duration}秒的短视频脚本：
        主题：{topic}
        
        要求：
        1. 开头要吸引人
        2. 内容要有价值
        3. 结尾要有号召性
        4. 适合抖音平台
        5. 包含具体的镜头描述和台词
        
        请按以下格式输出：
        标题：[视频标题]
        时长：{duration}秒
        脚本：
        [详细的分镜头脚本]
        """
        
        return await self.generate_text(prompt, max_tokens=1000)
    
    async def generate_video_title(self, content: str) -> Dict:
        """生成视频标题"""
        prompt = f"""
        请为以下视频内容生成5个吸引人的抖音标题：
        
        视频内容：{content}
        
        要求：
        1. 标题要吸引人
        2. 适合抖音平台
        3. 包含热门话题标签
        4. 长度适中（15-30字）
        5. 有情感共鸣
        
        请按以下格式输出：
        1. [标题1]
        2. [标题2]
        3. [标题3]
        4. [标题4]
        5. [标题5]
        """
        
        return await self.generate_text(prompt, max_tokens=300)
    
    async def generate_video_description(self, title: str, content: str) -> Dict:
        """生成视频描述"""
        prompt = f"""
        请为以下视频生成抖音描述：
        
        标题：{title}
        内容：{content}
        
        要求：
        1. 描述要吸引人
        2. 包含相关话题标签
        3. 引导用户互动
        4. 长度适中（100-200字）
        5. 符合抖音平台规范
        
        请按以下格式输出：
        描述：[视频描述]
        话题标签：[#话题1 #话题2 #话题3]
        """
        
        return await self.generate_text(prompt, max_tokens=400) 