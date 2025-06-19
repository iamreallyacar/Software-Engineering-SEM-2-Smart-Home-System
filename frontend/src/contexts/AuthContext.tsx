/**
 * Authentication context for managing user login state
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authAPI } from '../services/api';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  // Check for existing authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('user');

      if (token && savedUser) {
        try {
          // Verify token is still valid
          const currentUser = await authAPI.getCurrentUser();
          setUser(currentUser.user || JSON.parse(savedUser));
        } catch (error) {
          // Token is invalid, clear storage
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login(username, password);
      
      if (response.key) {
        // Store auth token
        localStorage.setItem('authToken', response.key);
        
        // Get user info
        const userInfo = await authAPI.getCurrentUser();
        const userData = userInfo.user || {
          id: Date.now(), // Fallback if no user data
          username,
          email: '',
        };
        
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
      } else {
        throw new Error('No authentication token received');
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.detail || 
                          error.message || 
                          'Login failed';
      throw new Error(errorMessage);
    }
  };

  const register = async (username: string, email: string, password: string) => {
    try {
      const response = await authAPI.register(username, email, password);
      
      if (response.key) {
        // Store auth token
        localStorage.setItem('authToken', response.key);
        
        // Get user info
        const userInfo = await authAPI.getCurrentUser();
        const userData = userInfo.user || {
          id: Date.now(), // Fallback if no user data
          username,
          email,
        };
        
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
      } else {
        throw new Error('No authentication token received');
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.detail ||
                          error.response?.data?.username?.[0] ||
                          error.response?.data?.email?.[0] ||
                          error.response?.data?.password?.[0] ||
                          error.message || 
                          'Registration failed';
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    // Call logout API (optional, for server-side cleanup)
    authAPI.logout().catch(() => {
      // Ignore errors on logout
    });

    // Clear local storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
