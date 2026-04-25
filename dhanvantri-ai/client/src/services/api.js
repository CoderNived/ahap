import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor — runs before every request
api.interceptors.request.use(
  (config) => {
    // Auth token will be added here in Phase 3
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — runs after every response
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.message ||
      'Something went wrong';
    return Promise.reject(new Error(message));
  }
);

export default api;