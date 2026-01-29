'use client';

import { useState, useEffect } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import {
  AcademicCapIcon,
  BookOpenIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  SparklesIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { useAuth } from '../../contexts/AuthContext';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  useEffect(() => {
    setTimeout(() => {
      setStats({
        totalCourses: 12,
        enrolledCourses: 5,
        completedCourses: 2,
        totalHours: 48,
        streak: 7,
        avgScore: 87,
        weeklyActivity: [
          { day: 'Mon', hours: 2 },
          { day: 'Tue', hours: 3 },
          { day: 'Wed', hours: 1.5 },
          { day: 'Thu', hours: 4 },
          { day: 'Fri', hours: 2.5 },
          { day: 'Sat', hours: 3.5 },
          { day: 'Sun', hours: 1 }
        ],
        courseProgress: [
          { name: 'Math Fundamentals', progress: 75 },
          { name: 'Programming', progress: 60 },
          { name: 'Data Structures', progress: 45 },
          { name: 'Web Dev', progress: 90 }
        ],
        scores: [
          { assignment: 'Quiz 1', score: 92 },
          { assignment: 'HW 1', score: 85 },
          { assignment: 'Midterm', score: 88 },
          { assignment: 'Quiz 2', score: 95 },
          { assignment: 'Final', score: 90 }
        ],
        recentCourses: [
          {
            id: 1,
            title: 'Mathematics Fundamentals',
            progress: 75,
            image: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=100&h=100&fit=crop'
          },
          {
            id: 2,
            title: 'Programming Basics',
            progress: 60,
            image: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=100&h=100&fit=crop'
          },
          {
            id: 5,
            title: 'Web Development',
            progress: 45,
            image: 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=100&h=100&fit=crop'
          }
        ]
      });
      setLoading(false);
    }, 500);
  }, []);

  const weeklyActivityData = {
    labels: stats?.weeklyActivity.map((item: any) => item.day) || [],
    datasets: [
      {
        label: 'Hours',
        data: stats?.weeklyActivity.map((item: any) => item.hours) || [],
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 0,
        borderRadius: 4,
      },
    ],
  };

  const courseProgressData = {
    labels: stats?.courseProgress.map((item: any) => item.name) || [],
    datasets: [
      {
        label: 'Progress',
        data: stats?.courseProgress.map((item: any) => item.progress) || [],
        backgroundColor: [
          'rgba(59, 130, 246, 0.7)',
          'rgba(16, 185, 129, 0.7)',
          'rgba(245, 158, 11, 0.7)',
          'rgba(139, 92, 246, 0.7)',
        ],
        borderRadius: 4,
      },
    ],
  };

  const scoreData = {
    labels: stats?.scores.map((item: any) => item.assignment) || [],
    datasets: [
      {
        label: 'Score',
        data: stats?.scores.map((item: any) => item.score) || [],
        fill: true,
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderColor: 'rgb(16, 185, 129)',
        tension: 0.4,
        pointBackgroundColor: 'rgb(16, 185, 129)',
        pointRadius: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 11 } }
      },
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.05)' },
        ticks: { font: { size: 11 } }
      }
    }
  };

  if (loading || authLoading) {
    return (
      <div className="dashboard-container">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-2/3 sm:w-1/3"></div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white p-4 sm:p-6 rounded-xl h-24 sm:h-28"></div>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <div key={i} className="bg-white p-4 sm:p-6 rounded-xl h-64 sm:h-80"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
          {getGreeting()}, {user?.name?.split(' ')[0] || 'there'}!
        </h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Track your progress and continue learning</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 sm:p-3 rounded-lg bg-blue-100 shrink-0">
              <AcademicCapIcon className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600 truncate">Enrolled</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.enrolledCourses}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 sm:p-3 rounded-lg bg-green-100 shrink-0">
              <BookOpenIcon className="h-5 w-5 sm:h-6 sm:w-6 text-green-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600 truncate">Completed</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.completedCourses}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 sm:p-3 rounded-lg bg-yellow-100 shrink-0">
              <ClockIcon className="h-5 w-5 sm:h-6 sm:w-6 text-yellow-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600 truncate">Hours</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.totalHours}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center">
            <div className="p-2 sm:p-3 rounded-lg bg-purple-100 shrink-0">
              <ArrowTrendingUpIcon className="h-5 w-5 sm:h-6 sm:w-6 text-purple-600" />
            </div>
            <div className="ml-3 min-w-0">
              <p className="text-xs sm:text-sm text-gray-600 truncate">Streak</p>
              <p className="text-xl sm:text-2xl font-bold text-gray-900">{stats.streak} <span className="text-sm font-normal">days</span></p>
            </div>
          </div>
        </div>
      </div>

      {/* Continue Learning */}
      <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 mb-6 sm:mb-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900">Continue Learning</h3>
          <Link href="/courses" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center">
            View all <ChevronRightIcon className="h-4 w-4 ml-1" />
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
          {stats.recentCourses.map((course: any) => (
            <Link
              key={course.id}
              href={`/courses/${course.id}`}
              className="flex items-center p-3 sm:p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <img
                src={course.image}
                alt={course.title}
                className="w-12 h-12 sm:w-14 sm:h-14 rounded-lg object-cover shrink-0"
              />
              <div className="ml-3 flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 text-sm sm:text-base truncate">{course.title}</h4>
                <div className="mt-1.5">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Progress</span>
                    <span>{course.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-blue-600 h-1.5 rounded-full"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Weekly Activity</h3>
          <div className="h-48 sm:h-56">
            <Bar data={weeklyActivityData} options={chartOptions} />
          </div>
        </div>

        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Course Progress</h3>
          <div className="h-48 sm:h-56">
            <Bar
              data={courseProgressData}
              options={{
                ...chartOptions,
                indexAxis: 'y',
                scales: {
                  ...chartOptions.scales,
                  x: { ...chartOptions.scales.x, max: 100 }
                }
              }}
            />
          </div>
        </div>
      </div>

      {/* Score Trend & Premium */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Score Trends</h3>
          <div className="h-48 sm:h-56">
            <Line
              data={scoreData}
              options={{
                ...chartOptions,
                scales: {
                  ...chartOptions.scales,
                  y: { ...chartOptions.scales.y, min: 60, max: 100 }
                }
              }}
            />
          </div>
        </div>

        {/* Premium Card */}
        <div className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-5 sm:p-6 rounded-xl text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16" />
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full -ml-12 -mb-12" />

          <div className="relative">
            <div className="flex items-center mb-3 sm:mb-4">
              <SparklesIcon className="h-6 w-6 sm:h-7 sm:w-7 mr-2" />
              <h3 className="text-lg sm:text-xl font-bold">Premium Features</h3>
            </div>
            <p className="mb-4 sm:mb-5 opacity-90 text-sm sm:text-base">Unlock AI-powered learning tools</p>
            <ul className="space-y-2 sm:space-y-2.5 mb-5 sm:mb-6 text-sm sm:text-base">
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-green-400 rounded-full mr-2.5" />
                Adaptive Learning Paths
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-green-400 rounded-full mr-2.5" />
                AI-Graded Assessments
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-green-400 rounded-full mr-2.5" />
                Cross-Chapter Synthesis
              </li>
            </ul>
            <Link
              href="/subscription"
              className="inline-block bg-white text-blue-600 px-5 sm:px-6 py-2 sm:py-2.5 rounded-lg font-medium hover:bg-blue-50 transition-colors text-sm sm:text-base"
            >
              {user?.subscription === 'premium' ? 'Manage Plan' : 'Upgrade Now'}
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {[
            { icon: BookOpenIcon, iconBg: 'bg-green-100', iconColor: 'text-green-600', title: 'Completed "Intro to Algorithms"', time: '2 hours ago', badge: 'Completed', badgeColor: 'bg-green-100 text-green-800' },
            { icon: AcademicCapIcon, iconBg: 'bg-blue-100', iconColor: 'text-blue-600', title: 'Started "Advanced JavaScript"', time: '5 hours ago', badge: 'In Progress', badgeColor: 'bg-blue-100 text-blue-800' },
            { icon: ClockIcon, iconBg: 'bg-yellow-100', iconColor: 'text-yellow-600', title: 'Submitted Assignment 3', time: '1 day ago', badge: 'Pending', badgeColor: 'bg-yellow-100 text-yellow-800' },
          ].map((item, i) => (
            <div key={i} className="flex items-center justify-between p-3 sm:p-4 hover:bg-gray-50 rounded-lg transition-colors">
              <div className="flex items-center min-w-0">
                <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-full ${item.iconBg} flex items-center justify-center shrink-0`}>
                  <item.icon className={`h-4 w-4 sm:h-5 sm:w-5 ${item.iconColor}`} />
                </div>
                <div className="ml-3 min-w-0">
                  <p className="font-medium text-gray-900 text-sm sm:text-base truncate">{item.title}</p>
                  <p className="text-xs sm:text-sm text-gray-500">{item.time}</p>
                </div>
              </div>
              <span className={`${item.badgeColor} px-2 sm:px-3 py-1 rounded-full text-xs font-medium shrink-0 ml-2`}>
                {item.badge}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
