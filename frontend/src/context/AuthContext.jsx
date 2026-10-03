import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check active session on initial load
  useEffect(() => {
    async function checkAuth() {
      try {
        const currentUser = await authApi.me();
        setUser(currentUser);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  const login = async (usernameOrEmail, password) => {
    const res = await authApi.login({
      username_or_email: usernameOrEmail,
      password: password,
    });
    setUser(res.user);
    return res.user;
  };

  const register = async (userData) => {
    const res = await authApi.register(userData);
    setUser(res.user);
    return res.user;
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } finally {
      setUser(null);
    }
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    refreshUser: async () => {
      try {
        const u = await authApi.me();
        setUser(u);
      } catch {
        setUser(null);
      }
    }
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
