'use client';

import { usePathname } from 'next/navigation';
import Sidebar from './Sidebar';
import { AuthProvider } from '../contexts/AuthContext';

// Pages that should not show sidebar
const authPages = ['/login', '/register', '/'];

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isAuthPage = authPages.includes(pathname);

  return (
    <AuthProvider>
      {isAuthPage ? (
        // Auth pages - no sidebar
        <main className="min-h-screen">{children}</main>
      ) : (
        // App pages - with sidebar
        <div className="min-h-screen bg-gray-50">
          <Sidebar />
          {/* Main content area */}
          <div className="lg:pl-64">
            {/* Mobile header spacer */}
            <div className="h-16 lg:hidden" />
            {/* Main content */}
            <main className="min-h-[calc(100vh-4rem)] lg:min-h-screen">
              {children}
            </main>
          </div>
        </div>
      )}
    </AuthProvider>
  );
}
