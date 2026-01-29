'use client';

import { useState } from 'react';
import {
  ChartBarIcon,
  ClockIcon,
  FireIcon,
  TrophyIcon,
  BookOpenIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

interface CourseProgress {
  id: string;
  title: string;
  progress: number;
  lessonsCompleted: number;
  totalLessons: number;
  lastAccessed: string;
}

export default function ProgressPage() {
  const [stats] = useState({
    totalHours: 42,
    coursesCompleted: 5,
    currentStreak: 7,
    certificatesEarned: 3
  });

  const [courses] = useState<CourseProgress[]>([
    { id: '1', title: 'Web Development Fundamentals', progress: 75, lessonsCompleted: 15, totalLessons: 20, lastAccessed: '2 hours ago' },
    { id: '2', title: 'Advanced JavaScript', progress: 45, lessonsCompleted: 9, totalLessons: 20, lastAccessed: 'Yesterday' },
    { id: '3', title: 'React Essentials', progress: 20, lessonsCompleted: 4, totalLessons: 20, lastAccessed: '3 days ago' },
    { id: '4', title: 'Node.js Backend Development', progress: 100, lessonsCompleted: 18, totalLessons: 18, lastAccessed: 'Last week' }
  ]);

  const [weeklyActivity] = useState([
    { day: 'Mon', hours: 2.5 },
    { day: 'Tue', hours: 1.5 },
    { day: 'Wed', hours: 3 },
    { day: 'Thu', hours: 2 },
    { day: 'Fri', hours: 1 },
    { day: 'Sat', hours: 4 },
    { day: 'Sun', hours: 2 }
  ]);

  const maxHours = Math.max(...weeklyActivity.map(d => d.hours));

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Your Progress</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Track your learning journey</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-blue-100 rounded-full flex items-center justify-center shrink-0">
              <ClockIcon className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600">Learning Time</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.totalHours}h</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-green-100 rounded-full flex items-center justify-center shrink-0">
              <CheckCircleIcon className="h-5 w-5 sm:h-6 sm:w-6 text-green-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600">Completed</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.coursesCompleted}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-orange-100 rounded-full flex items-center justify-center shrink-0">
              <FireIcon className="h-5 w-5 sm:h-6 sm:w-6 text-orange-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600">Streak</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.currentStreak} <span className="text-sm font-normal">days</span></p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-purple-100 rounded-full flex items-center justify-center shrink-0">
              <TrophyIcon className="h-5 w-5 sm:h-6 sm:w-6 text-purple-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600">Certificates</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.certificatesEarned}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
        {/* Weekly Activity */}
        <div className="lg:col-span-1 bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Weekly Activity</h3>
          <div className="flex items-end justify-between h-32 sm:h-40 gap-1 sm:gap-2">
            {weeklyActivity.map((day) => (
              <div key={day.day} className="flex flex-col items-center flex-1">
                <div
                  className="w-full bg-blue-500 rounded-t transition-all hover:bg-blue-600"
                  style={{ height: `${(day.hours / maxHours) * 100}%`, minHeight: '8px' }}
                />
                <span className="text-xs text-gray-500 mt-2">{day.day}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-100 text-center">
            <p className="text-xs sm:text-sm text-gray-600">This Week</p>
            <p className="text-lg sm:text-xl font-bold text-gray-900">
              {weeklyActivity.reduce((sum, d) => sum + d.hours, 0)} hours
            </p>
          </div>
        </div>

        {/* Course Progress */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base sm:text-lg font-semibold text-gray-900">Course Progress</h3>
            <BookOpenIcon className="h-5 w-5 text-gray-400" />
          </div>

          <div className="space-y-4 sm:space-y-5">
            {courses.map((course) => (
              <div key={course.id}>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 sm:gap-2 mb-2">
                  <div className="min-w-0">
                    <h4 className="font-medium text-gray-900 text-sm sm:text-base truncate">{course.title}</h4>
                    <p className="text-xs text-gray-500">
                      {course.lessonsCompleted}/{course.totalLessons} lessons • {course.lastAccessed}
                    </p>
                  </div>
                  <span className={`font-medium text-sm shrink-0 ${
                    course.progress === 100 ? 'text-green-600' : 'text-blue-600'
                  }`}>
                    {course.progress}%
                  </span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      course.progress === 100 ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${course.progress}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Achievements */}
      <div className="mt-4 sm:mt-6 lg:mt-8 bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
        <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Recent Achievements</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
          <div className="flex items-center p-3 sm:p-4 bg-yellow-50 rounded-lg">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-yellow-100 rounded-full flex items-center justify-center shrink-0">
              <TrophyIcon className="h-5 w-5 sm:h-6 sm:w-6 text-yellow-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="font-medium text-gray-900 text-sm sm:text-base truncate">First Course Completed</p>
              <p className="text-xs text-gray-500">2 weeks ago</p>
            </div>
          </div>
          <div className="flex items-center p-3 sm:p-4 bg-blue-50 rounded-lg">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-blue-100 rounded-full flex items-center justify-center shrink-0">
              <FireIcon className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="font-medium text-gray-900 text-sm sm:text-base truncate">7-Day Streak</p>
              <p className="text-xs text-gray-500">Today</p>
            </div>
          </div>
          <div className="flex items-center p-3 sm:p-4 bg-green-50 rounded-lg sm:col-span-2 lg:col-span-1">
            <div className="h-10 w-10 sm:h-12 sm:w-12 bg-green-100 rounded-full flex items-center justify-center shrink-0">
              <ChartBarIcon className="h-5 w-5 sm:h-6 sm:w-6 text-green-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="font-medium text-gray-900 text-sm sm:text-base truncate">10 Hours Milestone</p>
              <p className="text-xs text-gray-500">1 week ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
