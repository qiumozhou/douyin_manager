import api from './index';

export const getDouyinVideos = () => api.get('/douyin/videos');
export const publishVideoToDouyin = (videoId) => api.post(`/douyin/publish/${videoId}`);
export const getPublishStatus = (taskId) => api.get(`/douyin/publish/status/${taskId}`); 