'use client';

import { useState, useEffect } from 'react';
import {
  HomeIcon,
  AcademicCapIcon,
  BookOpenIcon,
  ChartBarIcon,
  CogIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  CreditCardIcon,
  Bars3Icon,
  XMarkIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Courses', href: '/courses', icon: AcademicCapIcon },
  { name: 'Learning Path', href: '/learning-path', icon: BookOpenIcon },
  { name: 'Progress', href: '/progress', icon: ChartBarIcon },
  { name: 'Premium', href: '/premium', icon: SparklesIcon },
  { name: 'Profile', href: '/profile', icon: UserIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
  { name: 'Subscription', href: '/subscription', icon: CreditCardIcon },
];

export default function Sidebar() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();
  const { user, logout, isLoading } = useAuth();

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  // Close sidebar on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setSidebarOpen(false);
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  const isActive = (href: string) => pathname === href;

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  if (isLoading) {
    return (
      <>
        {/* Mobile placeholder */}
        <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-40" />
        {/* Desktop placeholder */}
        <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:flex lg:w-64 lg:flex-col bg-white border-r border-gray-200">
          <div className="animate-pulse p-4 space-y-4">
            <div className="h-8 bg-gray-200 rounded w-32" />
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-10 bg-gray-200 rounded" />
            ))}
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      {/* Mobile Header Bar */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-40 flex items-center justify-between px-4">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Open menu"
        >
          <Bars3Icon className="h-6 w-6 text-gray-600" />
        </button>

        <div className="flex items-center">
          <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
            <AcademicCapIcon className="h-5 w-5 text-white" />
          </div>
          <span className="ml-2 text-lg font-bold text-gray-900">Course Companion</span>
        </div>

        <Link href="/profile" className="p-2">
          <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
            <span className="text-blue-600 text-sm font-medium">
              {user ? getInitials(user.name) : 'U'}
            </span>
          </div>
        </Link>
      </div>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 z-50 bg-gray-900/50 backdrop-blur-sm"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Mobile Sidebar */}
      <div className={`lg:hidden fixed inset-y-0 left-0 z-50 w-72 bg-white transform transition-transform duration-300 ease-in-out ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-4 border-b border-gray-200">
            <div className="flex items-center">
              <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
                <AcademicCapIcon className="h-5 w-5 text-white" />
              </div>
              <span className="ml-3 text-lg font-bold text-gray-900">Course Companion</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              aria-label="Close menu"
            >
              <XMarkIcon className="h-6 w-6 text-gray-600" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4 px-3">
            <div className="space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-3 py-3 rounded-lg transition-colors ${
                    isActive(item.href)
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className={`h-5 w-5 mr-3 flex-shrink-0 ${
                    isActive(item.href) ? 'text-blue-600' : 'text-gray-400'
                  }`} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <button
                onClick={() => {
                  logout();
                  setSidebarOpen(false);
                }}
                className="w-full flex items-center px-3 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-5 w-5 mr-3 text-gray-400 flex-shrink-0" />
                <span className="font-medium">Sign out</span>
              </button>
            </div>
          </nav>

          {/* User Info */}
          <div className="p-4 border-t border-gray-200">
            <Link href="/profile" onClick={() => setSidebarOpen(false)} className="flex items-center">
              <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <span className="text-blue-600 font-medium">
                  {user ? getInitials(user.name) : 'U'}
                </span>
              </div>
              <div className="ml-3 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{user?.name || 'User'}</p>
                <p className="text-xs text-gray-500 truncate">{user?.email || ''}</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Desktop Sidebar - Fixed */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-30 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-gray-200 overflow-y-auto">
          {/* Header */}
          <div className="flex items-center flex-shrink-0 px-6 py-4 border-b border-gray-200">
            <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
              <AcademicCapIcon className="h-5 w-5 text-white" />
            </div>
            <span className="ml-3 text-lg font-bold text-gray-900">Course Companion</span>
          </div>

          {/* Navigation */}
          <nav className="flex-1 py-4 px-3">
            <div className="space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-3 py-2.5 rounded-lg transition-colors ${
                    isActive(item.href)
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className={`h-5 w-5 mr-3 flex-shrink-0 ${
                    isActive(item.href) ? 'text-blue-600' : 'text-gray-400'
                  }`} />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <button
                onClick={logout}
                className="w-full flex items-center px-3 py-2.5 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-5 w-5 mr-3 text-gray-400 flex-shrink-0" />
                <span className="text-sm font-medium">Sign out</span>
              </button>
            </div>
          </nav>

          {/* User Info */}
          <div className="flex-shrink-0 p-4 border-t border-gray-200">
            <Link href="/profile" className="flex items-center hover:bg-gray-50 rounded-lg p-2 -m-2 transition-colors">
              <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <span className="text-blue-600 font-medium">
                  {user ? getInitials(user.name) : 'U'}
                </span>
              </div>
              <div className="ml-3 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{user?.name || 'User'}</p>
                <p className="text-xs text-gray-500 capitalize">{user?.subscription || 'Free'} Member</p>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
