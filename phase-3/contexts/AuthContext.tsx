'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';

export interface User {
  id: string;
  name: string;
  email: string;
  subscription: 'free' | 'premium';
  avatar?: string;
  joinDate: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  loginWithGoogle: () => Promise<boolean>;
  loginWithFacebook: () => Promise<boolean>;
  register: (name: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Pages that don't require authentication
const publicPaths = ['/', '/login', '/register'];

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Check for existing session on mount
  useEffect(() => {
    const checkAuth = () => {
      try {
        const storedUser = localStorage.getItem('user');
        const token = localStorage.getItem('token');

        if (storedUser && token) {
          const userData = JSON.parse(storedUser);
          setUser(userData);
        }
      } catch (error) {
        console.error('Error checking auth:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Redirect logic
  useEffect(() => {
    if (!isLoading) {
      const isPublicPath = publicPaths.includes(pathname);

      if (!user && !isPublicPath) {
        router.push('/login');
      } else if (user && (pathname === '/login' || pathname === '/register')) {
        router.push('/dashboard');
      }
    }
  }, [user, isLoading, pathname, router]);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // For demo: Accept any valid email/password combo
      // In production, this would call the API
      const mockToken = btoa(`${email}:${Date.now()}`);
      const mockUser: User = {
        id: crypto.randomUUID(),
        name: email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        email: email,
        subscription: 'free',
        joinDate: new Date().toISOString().split('T')[0]
      };

      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);

      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const loginWithGoogle = async (): Promise<boolean> => {
    try {
      // Simulate Google OAuth delay
      await new Promise(resolve => setTimeout(resolve, 1500));

      // For demo: Create a mock Google user
      // In production, this would use Google OAuth
      const mockEmail = `user${Math.floor(Math.random() * 10000)}@gmail.com`;
      const mockToken = btoa(`google:${mockEmail}:${Date.now()}`);
      const mockUser: User = {
        id: crypto.randomUUID(),
        name: 'Google User',
        email: mockEmail,
        subscription: 'free',
        joinDate: new Date().toISOString().split('T')[0],
        avatar: `https://lh3.googleusercontent.com/a/default-user`
      };

      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      localStorage.setItem('authProvider', 'google');
      setUser(mockUser);

      return true;
    } catch (error) {
      console.error('Google login error:', error);
      return false;
    }
  };

  const loginWithFacebook = async (): Promise<boolean> => {
    try {
      // Simulate Facebook OAuth delay
      await new Promise(resolve => setTimeout(resolve, 1500));

      // For demo: Create a mock Facebook user
      // In production, this would use Facebook OAuth
      const mockEmail = `user${Math.floor(Math.random() * 10000)}@facebook.com`;
      const mockToken = btoa(`facebook:${mockEmail}:${Date.now()}`);
      const mockUser: User = {
        id: crypto.randomUUID(),
        name: 'Facebook User',
        email: mockEmail,
        subscription: 'free',
        joinDate: new Date().toISOString().split('T')[0],
        avatar: `https://graph.facebook.com/default/picture`
      };

      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      localStorage.setItem('authProvider', 'facebook');
      setUser(mockUser);

      return true;
    } catch (error) {
      console.error('Facebook login error:', error);
      return false;
    }
  };

  const register = async (name: string, email: string, password: string): Promise<boolean> => {
    try {
      // For demo: Create user locally
      // In production, this would call the API
      const mockToken = btoa(`${email}:${Date.now()}`);
      const mockUser: User = {
        id: crypto.randomUUID(),
        name: name,
        email: email,
        subscription: 'free',
        joinDate: new Date().toISOString().split('T')[0]
      };

      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);

      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('authProvider');
    setUser(null);
    router.push('/login');
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      setUser(updatedUser);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        loginWithGoogle,
        loginWithFacebook,
        register,
        logout,
        updateUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
