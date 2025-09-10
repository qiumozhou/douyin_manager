import api from './index';

export const register = (data) => api.post('/auth/register', data);
export const login = (data) => api.post('/auth/token', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
export const getMe = () => api.get('/auth/me');
export const getDouyinAuthUrl = () => api.get('/auth/douyin/auth');
export const douyinCallback = (code) => api.get(`/auth/douyin/callback?code=${code}`); 