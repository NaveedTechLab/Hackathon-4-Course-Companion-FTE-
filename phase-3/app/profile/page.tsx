'use client';

import { useState, useEffect } from 'react';
import { UserIcon, EnvelopeIcon, AcademicCapIcon, CalendarIcon, CreditCardIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';

export default function ProfilePage() {
  const { user, updateUser, isLoading } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [authProvider, setAuthProvider] = useState<string | null>(null);

  useEffect(() => {
    const provider = localStorage.getItem('authProvider');
    setAuthProvider(provider);
  }, []);

  const stats = {
    totalCourses: 12,
    completedCourses: 5,
    learningStreak: 7
  };

  const handleSaveProfile = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSaving(true);

    const formData = new FormData(e.currentTarget);
    const name = formData.get('name') as string;
    const email = formData.get('email') as string;

    updateUser({ name, email });

    setSaveMessage('Profile saved successfully!');
    setIsSaving(false);

    setTimeout(() => setSaveMessage(''), 3000);
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const tabs = ['overview', 'account', 'preferences', 'billing'];

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl h-72"></div>
            <div className="lg:col-span-2 bg-white p-6 rounded-xl h-72"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Your Profile</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 sm:p-6">
            <div className="text-center">
              <div className="mx-auto h-20 w-20 sm:h-24 sm:w-24 rounded-full bg-blue-100 flex items-center justify-center mb-4">
                <span className="text-2xl sm:text-3xl font-bold text-blue-600">
                  {user ? getInitials(user.name) : 'U'}
                </span>
              </div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900">{user?.name || 'User'}</h2>
              <p className="text-gray-600 text-sm">{user?.email || ''}</p>

              <div className="mt-3 flex flex-wrap justify-center gap-2">
                <div className="inline-flex items-center px-3 py-1 rounded-full text-xs sm:text-sm font-medium bg-blue-100 text-blue-800">
                  <AcademicCapIcon className="h-4 w-4 mr-1" />
                  {user?.subscription === 'premium' ? 'Premium' : 'Free'} Member
                </div>
                {authProvider && (
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${
                    authProvider === 'google' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'
                  }`}>
                    {authProvider === 'google' ? (
                      <svg className="h-3.5 w-3.5 mr-1" viewBox="0 0 24 24">
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                      </svg>
                    ) : (
                      <svg className="h-3.5 w-3.5 mr-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" />
                      </svg>
                    )}
                    {authProvider === 'google' ? 'Google' : 'Facebook'}
                  </div>
                )}
              </div>
            </div>

            <div className="mt-5 space-y-3">
              <div className="flex items-center text-gray-600 text-sm">
                <EnvelopeIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-3 text-gray-400 shrink-0" />
                <span className="truncate">{user?.email || ''}</span>
              </div>
              <div className="flex items-center text-gray-600 text-sm">
                <CalendarIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-3 text-gray-400 shrink-0" />
                <span>Joined {user?.joinDate ? new Date(user.joinDate).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'Recently'}</span>
              </div>
            </div>

            <div className="mt-5 pt-5 border-t border-gray-200">
              <h3 className="text-sm font-medium text-gray-900 mb-3">Learning Stats</h3>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-lg sm:text-xl font-bold text-gray-900">{stats.totalCourses}</p>
                  <p className="text-xs text-gray-500">Courses</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-lg sm:text-xl font-bold text-green-600">{stats.completedCourses}</p>
                  <p className="text-xs text-gray-500">Done</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-lg sm:text-xl font-bold text-purple-600">{stats.learningStreak}</p>
                  <p className="text-xs text-gray-500">Streak</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Content */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100">
            {/* Tabs */}
            <div className="border-b border-gray-200 overflow-x-auto scrollbar-hide">
              <nav className="flex px-4 sm:px-6 min-w-max">
                {tabs.map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`py-3 sm:py-4 px-3 sm:px-4 text-xs sm:text-sm font-medium capitalize whitespace-nowrap ${
                      activeTab === tab
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </nav>
            </div>

            <div className="p-4 sm:p-6">
              {activeTab === 'overview' && (
                <div>
                  <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-4">Learning Overview</h3>

                  <div className="grid grid-cols-3 gap-3 sm:gap-4 mb-6">
                    <div className="bg-blue-50 p-3 sm:p-4 rounded-lg text-center">
                      <div className="text-xl sm:text-2xl font-bold text-blue-600">{stats.totalCourses}</div>
                      <div className="text-xs sm:text-sm text-gray-600">Total</div>
                    </div>
                    <div className="bg-green-50 p-3 sm:p-4 rounded-lg text-center">
                      <div className="text-xl sm:text-2xl font-bold text-green-600">{stats.completedCourses}</div>
                      <div className="text-xs sm:text-sm text-gray-600">Completed</div>
                    </div>
                    <div className="bg-purple-50 p-3 sm:p-4 rounded-lg text-center">
                      <div className="text-xl sm:text-2xl font-bold text-purple-600">{stats.learningStreak}</div>
                      <div className="text-xs sm:text-sm text-gray-600">Day Streak</div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm sm:text-base font-medium text-gray-900 mb-3">Recent Activity</h4>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="min-w-0">
                          <p className="font-medium text-sm text-gray-900 truncate">Completed "Mathematics Fundamentals"</p>
                          <p className="text-xs text-gray-500">2 hours ago</p>
                        </div>
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium shrink-0 ml-2">Done</span>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="min-w-0">
                          <p className="font-medium text-sm text-gray-900 truncate">Started "Advanced JavaScript"</p>
                          <p className="text-xs text-gray-500">1 day ago</p>
                        </div>
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium shrink-0 ml-2">Active</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'account' && (
                <div>
                  <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-4">Account Settings</h3>

                  {saveMessage && (
                    <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
                      <p className="text-sm text-green-600">{saveMessage}</p>
                    </div>
                  )}

                  <form className="space-y-4 sm:space-y-5" onSubmit={handleSaveProfile}>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                      <input
                        type="text"
                        name="name"
                        defaultValue={user?.name || ''}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                      <input
                        type="email"
                        name="email"
                        defaultValue={user?.email || ''}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Change Password</label>
                      <div className="space-y-3">
                        <input
                          type="password"
                          placeholder="Current password"
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <input
                          type="password"
                          placeholder="New password"
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      disabled={isSaving}
                      className={`w-full sm:w-auto px-6 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                        isSaving
                          ? 'bg-blue-400 text-white cursor-not-allowed'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      {isSaving ? 'Saving...' : 'Save Changes'}
                    </button>
                  </form>
                </div>
              )}

              {activeTab === 'preferences' && (
                <div>
                  <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-4">Learning Preferences</h3>

                  <div className="space-y-5">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Learning Goals</label>
                      <textarea
                        rows={3}
                        placeholder="What are your learning goals?"
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Time</label>
                      <select className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                        <option>Morning (6 AM - 12 PM)</option>
                        <option>Afternoon (12 PM - 6 PM)</option>
                        <option>Evening (6 PM - 12 AM)</option>
                        <option>Any time</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Notifications</label>
                      <div className="space-y-3">
                        {['Email notifications', 'Push notifications', 'Weekly progress'].map((label) => (
                          <div key={label} className="flex items-center">
                            <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 rounded" />
                            <label className="ml-2 text-sm text-gray-700">{label}</label>
                          </div>
                        ))}
                      </div>
                    </div>

                    <button className="w-full sm:w-auto bg-blue-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                      Save Preferences
                    </button>
                  </div>
                </div>
              )}

              {activeTab === 'billing' && (
                <div>
                  <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-4">Billing Information</h3>

                  <div className="bg-gray-50 p-4 sm:p-5 rounded-lg mb-5">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                      <div>
                        <h4 className="font-medium text-gray-900 text-sm sm:text-base">
                          {user?.subscription === 'premium' ? 'Premium Subscription' : 'Free Plan'}
                        </h4>
                        <p className="text-gray-600 text-xs sm:text-sm">
                          {user?.subscription === 'premium' ? 'Renews Feb 15, 2024' : 'Upgrade to unlock premium'}
                        </p>
                      </div>
                      <div className="text-left sm:text-right">
                        <p className="font-medium text-sm sm:text-base">{user?.subscription === 'premium' ? '$19.99/mo' : 'Free'}</p>
                        {user?.subscription !== 'premium' && (
                          <a href="/subscription" className="text-sm text-blue-600 hover:text-blue-700">Upgrade</a>
                        )}
                      </div>
                    </div>
                  </div>

                  {user?.subscription === 'premium' && (
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Payment Method</h4>
                        <div className="flex items-center p-3 sm:p-4 border border-gray-200 rounded-lg">
                          <CreditCardIcon className="h-6 w-6 sm:h-8 sm:w-8 text-gray-400 mr-3 shrink-0" />
                          <div className="flex-1 min-w-0">
                            <p className="font-medium text-sm truncate">**** **** **** 4242</p>
                            <p className="text-xs text-gray-600">Expires 12/2025</p>
                          </div>
                          <button className="text-xs sm:text-sm text-blue-600 shrink-0">Change</button>
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-medium text-gray-900 mb-2">History</h4>
                        <div className="space-y-2">
                          {['Jan 15, 2024', 'Dec 15, 2023'].map((date) => (
                            <div key={date} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                              <div>
                                <p className="font-medium text-sm">Premium</p>
                                <p className="text-xs text-gray-500">{date}</p>
                              </div>
                              <span className="font-medium text-sm">$19.99</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
