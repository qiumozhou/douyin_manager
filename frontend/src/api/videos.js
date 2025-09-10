import api from './index';

export const listVideos = (params) => api.get('/videos', { params });
export const uploadVideo = (formData) => api.post('/videos/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const getVideo = (id) => api.get(`/videos/${id}`);
export const updateVideo = (id, data) => api.put(`/videos/${id}`, data);
export const deleteVideo = (id) => api.delete(`/videos/${id}`); 