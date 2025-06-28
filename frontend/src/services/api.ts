import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/auth/login/', credentials),
  
  register: (userData: { username: string; email: string; password: string; password_confirm: string }) =>
    api.post('/auth/register/', userData),
  
  logout: () => api.post('/auth/logout/'),
};

// Activities API
export const activitiesAPI = {
  getAll: () => api.get('/activities/'),
  create: (activity: any) => api.post('/activities/', activity),
  update: (id: number, activity: any) => api.put(`/activities/${id}/`, activity),
  delete: (id: number) => api.delete(`/activities/${id}/`),
  toggleActive: (id: number) => api.post(`/activities/${id}/toggle_active/`),
  getCategories: () => api.get('/activities/categories/'),
};

// Grid API
export const gridAPI = {
  getByDate: (date: string) => api.get(`/grids/${date}/`),
  create: (gridData: any) => api.post('/grids/', gridData),
  logActivity: (gridId: number, data: { activity_id: number; position: number }) =>
    api.post(`/grids/${gridId}/log_activity/`, data),
  getRange: (startDate: string, endDate: string) =>
    api.get(`/grids/range/${startDate}/${endDate}/`),
};

// Analytics API
export const analyticsAPI = {
  getOverview: () => api.get('/analytics/overview/'),
  getStreaks: () => api.get('/analytics/streaks/'),
  getCompletionRates: () => api.get('/analytics/completion_rates/'),
  getPatterns: () => api.get('/analytics/patterns/'),
  getWeeklyReport: () => api.get('/analytics/weekly_report/'),
};

// Profile API
export const profileAPI = {
  get: () => api.get('/profile/'),
  update: (userData: any) => api.put('/profile/', userData),
};

export default api; 