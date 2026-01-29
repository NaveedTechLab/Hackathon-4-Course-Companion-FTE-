'use client';

import { useState } from 'react';
import {
  BellIcon,
  ShieldCheckIcon,
  PaintBrushIcon
} from '@heroicons/react/24/outline';

export default function SettingsPage() {
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    weeklyDigest: true,
    courseUpdates: true,
    promotions: false
  });

  const [appearance, setAppearance] = useState({
    theme: 'light',
    fontSize: 'medium',
    reducedMotion: false
  });

  const [privacy, setPrivacy] = useState({
    profileVisibility: 'public',
    showProgress: true,
    showAchievements: true
  });

  const Toggle = ({ enabled, onChange }: { enabled: boolean; onChange: () => void }) => (
    <button
      onClick={onChange}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
        enabled ? 'bg-blue-600' : 'bg-gray-200'
      }`}
    >
      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
        enabled ? 'translate-x-6' : 'translate-x-1'
      }`} />
    </button>
  );

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Manage your preferences</p>
      </div>

      <div className="space-y-4 sm:space-y-6">
        {/* Notifications */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <div className="flex items-center mb-4 sm:mb-6">
            <BellIcon className="h-5 w-5 sm:h-6 sm:w-6 text-gray-400 mr-2 sm:mr-3" />
            <h2 className="text-base sm:text-lg font-semibold text-gray-900">Notifications</h2>
          </div>

          <div className="space-y-4">
            {[
              { key: 'email', label: 'Email Notifications', desc: 'Receive updates via email' },
              { key: 'push', label: 'Push Notifications', desc: 'Get push notifications' },
              { key: 'weeklyDigest', label: 'Weekly Digest', desc: 'Weekly progress summary' },
              { key: 'courseUpdates', label: 'Course Updates', desc: 'Content update notifications' },
              { key: 'promotions', label: 'Promotions', desc: 'Offers and promotions' }
            ].map((item, idx, arr) => (
              <div key={item.key} className={`flex items-center justify-between py-3 ${
                idx < arr.length - 1 ? 'border-b border-gray-100' : ''
              }`}>
                <div className="min-w-0 mr-4">
                  <p className="font-medium text-gray-900 text-sm sm:text-base">{item.label}</p>
                  <p className="text-xs sm:text-sm text-gray-500">{item.desc}</p>
                </div>
                <Toggle
                  enabled={notifications[item.key as keyof typeof notifications]}
                  onChange={() => setNotifications(prev => ({ ...prev, [item.key]: !prev[item.key as keyof typeof notifications] }))}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Appearance */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <div className="flex items-center mb-4 sm:mb-6">
            <PaintBrushIcon className="h-5 w-5 sm:h-6 sm:w-6 text-gray-400 mr-2 sm:mr-3" />
            <h2 className="text-base sm:text-lg font-semibold text-gray-900">Appearance</h2>
          </div>

          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Theme</label>
              <div className="flex flex-wrap gap-2 sm:gap-3">
                {['light', 'dark', 'system'].map((theme) => (
                  <button
                    key={theme}
                    onClick={() => setAppearance(prev => ({ ...prev, theme }))}
                    className={`px-3 sm:px-4 py-2 rounded-lg border capitalize text-sm transition-colors ${
                      appearance.theme === theme
                        ? 'border-blue-600 bg-blue-50 text-blue-600'
                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {theme}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Font Size</label>
              <select
                value={appearance.fontSize}
                onChange={(e) => setAppearance(prev => ({ ...prev, fontSize: e.target.value }))}
                className="w-full sm:w-48 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>

            <div className="flex items-center justify-between py-3">
              <div className="min-w-0 mr-4">
                <p className="font-medium text-gray-900 text-sm sm:text-base">Reduced Motion</p>
                <p className="text-xs sm:text-sm text-gray-500">Minimize animations</p>
              </div>
              <Toggle
                enabled={appearance.reducedMotion}
                onChange={() => setAppearance(prev => ({ ...prev, reducedMotion: !prev.reducedMotion }))}
              />
            </div>
          </div>
        </div>

        {/* Privacy */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <div className="flex items-center mb-4 sm:mb-6">
            <ShieldCheckIcon className="h-5 w-5 sm:h-6 sm:w-6 text-gray-400 mr-2 sm:mr-3" />
            <h2 className="text-base sm:text-lg font-semibold text-gray-900">Privacy</h2>
          </div>

          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Profile Visibility</label>
              <select
                value={privacy.profileVisibility}
                onChange={(e) => setPrivacy(prev => ({ ...prev, profileVisibility: e.target.value }))}
                className="w-full sm:w-48 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="public">Public</option>
                <option value="friends">Friends Only</option>
                <option value="private">Private</option>
              </select>
            </div>

            <div className="flex items-center justify-between py-3 border-t border-gray-100">
              <div className="min-w-0 mr-4">
                <p className="font-medium text-gray-900 text-sm sm:text-base">Show Progress</p>
                <p className="text-xs sm:text-sm text-gray-500">Let others see your progress</p>
              </div>
              <Toggle
                enabled={privacy.showProgress}
                onChange={() => setPrivacy(prev => ({ ...prev, showProgress: !prev.showProgress }))}
              />
            </div>

            <div className="flex items-center justify-between py-3 border-t border-gray-100">
              <div className="min-w-0 mr-4">
                <p className="font-medium text-gray-900 text-sm sm:text-base">Show Achievements</p>
                <p className="text-xs sm:text-sm text-gray-500">Display achievements publicly</p>
              </div>
              <Toggle
                enabled={privacy.showAchievements}
                onChange={() => setPrivacy(prev => ({ ...prev, showAchievements: !prev.showAchievements }))}
              />
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button className="w-full sm:w-auto bg-blue-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
