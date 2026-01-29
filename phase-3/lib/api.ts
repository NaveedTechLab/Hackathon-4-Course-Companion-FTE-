import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const PREMIUM_API_URL = process.env.NEXT_PUBLIC_PREMIUM_API_URL || 'http://localhost:8001';

// Create axios instances
export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const premiumApi = axios.create({
  baseURL: `${PREMIUM_API_URL}/api/v2/premium`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

premiumApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API functions
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { username: email, password }),
  me: () => api.get('/auth/me'),
};

export const coursesAPI = {
  getAll: () => api.get('/courses'),
  getById: (id: string) => api.get(`/courses/${id}`),
  getStructure: (id: string) => api.get(`/courses/${id}/structure`),
};

export const contentAPI = {
  getById: (id: string) => api.get(`/content/${id}`),
  stream: (id: string) => api.get(`/content/${id}/stream`),
};

export const progressAPI = {
  getProgress: (userId: string) => api.get(`/progress/${userId}`),
  updateProgress: (data: any) => api.put('/progress', data),
};

export const premiumAPI = {
  getAdaptiveLearning: (data: any) =>
    premiumApi.post('/adaptive-learning/generate', data),
  gradeAssessment: (data: any) =>
    premiumApi.post('/assessments/grade', data),
  getSynthesis: (data: any) =>
    premiumApi.post('/synthesis/connect-concepts', data),
};

export default api;
