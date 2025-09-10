import api from './index';

export const generateText = (prompt) => api.post('/ai/text', { prompt });
export const generateTitle = (content) => api.post('/ai/title', { content });
export const generateDescription = (title, content) => api.post('/ai/description', { title, content });
export const generateImage = (prompt, model = 'stable-diffusion') => api.post('/ai/image', { prompt, model }); 