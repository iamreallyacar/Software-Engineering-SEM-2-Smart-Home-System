/**
 * API service for communicating with the Django backend
 */

import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear invalid token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  },

  register: async (username: string, email: string, password: string) => {
    const response = await api.post('/auth/register/', { username, email, password });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout/');
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/user/');
    return response.data;
  },
};

// Smart Home API
export const smartHomeAPI = {
  getHomes: async () => {
    const response = await api.get('/smarthomes/');
    return response.data;
  },

  createHome: async (name: string, joinPassword?: string) => {
    const response = await api.post('/create-smarthome/', { 
      name, 
      join_password: joinPassword || '' 
    });
    return response.data;
  },

  joinHome: async (homeName: string, password: string) => {
    const response = await api.post('/join-smarthome/', { 
      home_name: homeName, 
      password 
    });
    return response.data;
  },

  leaveHome: async (homeId: number) => {
    const response = await api.post('/leave-smarthome/', { smart_home_id: homeId });
    return response.data;
  },

  getMembers: async (homeId: number) => {
    const response = await api.get(`/smarthome-members/?home_id=${homeId}`);
    return response.data;
  },
};

// Rooms API
export const roomsAPI = {
  getRooms: async () => {
    const response = await api.get('/rooms/');
    return response.data;
  },

  unlockRoom: async (homeId: number, roomId: number) => {
    const response = await api.post('/unlock-room/', { 
      smart_home_id: homeId, 
      room_id: roomId 
    });
    return response.data;
  },
};

// Devices API
export const devicesAPI = {
  getDevices: async () => {
    const response = await api.get('/devices/');
    return response.data;
  },

  getSupportedDevices: async () => {
    const response = await api.get('/supported-devices/');
    return response.data;
  },

  addDevice: async (roomId: number, supportedDeviceId: number, name: string) => {
    const response = await api.post('/add-device/', {
      room_id: roomId,
      supported_device_id: supportedDeviceId,
      name,
    });
    return response.data;
  },

  updateDevice: async (deviceId: number, data: { status?: boolean; analogue_value?: number }) => {
    const response = await api.patch(`/devices/${deviceId}/`, data);
    return response.data;
  },

  controlDevice: async (deviceId: number, status?: boolean, analogueValue?: number) => {
    const data: any = { device_id: deviceId };
    if (status !== undefined) data.status = status;
    if (analogueValue !== undefined) data.analogue_value = analogueValue;
    
    const response = await api.post('/device-control/', data);
    return response.data;
  },
};

// Demo API - New endpoints for demonstration features
export const demoAPI = {
  getEnergyDashboard: async () => {
    const response = await api.get('/demo/energy-dashboard/');
    return response.data;
  },

  runScenario: async (scenario: string) => {
    const response = await api.post('/demo/run-scenario/', { scenario });
    return response.data;
  },

  getAvailableScenarios: async () => {
    const response = await api.get('/demo/scenarios/');
    return response.data;
  },

  getDeviceEnergyDetails: async (deviceId: number) => {
    const response = await api.get(`/demo/device/${deviceId}/energy/`);
    return response.data;
  },

  getEnergyTrends: async (hours: number = 2) => {
    const response = await api.get(`/demo/energy-trends/?hours=${hours}`);
    return response.data;
  },

  simulateActivity: async () => {
    const response = await api.post('/demo/simulate-activity/');
    return response.data;
  },
};

// User API
export const userAPI = {
  getDashboardSummary: async () => {
    const response = await api.get('/dashboard-summary/');
    return response.data;
  },

  getCurrentUserInfo: async () => {
    const response = await api.get('/current-user/');
    return response.data;
  },
};

export default api;
