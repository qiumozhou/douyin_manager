import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8001/api/v1',
  timeout: 10000,
});

// 请求拦截器，可自动添加token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => Promise.reject(error));

export default api; 