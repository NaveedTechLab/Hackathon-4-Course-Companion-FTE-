'use client';

import { useState } from 'react';
import {
  AcademicCapIcon,
  CheckCircleIcon,
  ClockIcon,
  LockClosedIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import Link from 'next/link';

interface PathItem {
  id: string;
  title: string;
  description: string;
  duration: string;
  status: 'completed' | 'current' | 'locked';
  type: 'lesson' | 'quiz' | 'project';
}

interface LearningPath {
  id: string;
  title: string;
  description: string;
  progress: number;
  items: PathItem[];
}

export default function LearningPathPage() {
  const [activePath] = useState<LearningPath>({
    id: '1',
    title: 'Web Development Fundamentals',
    description: 'Master the core technologies of web development',
    progress: 35,
    items: [
      {
        id: '1',
        title: 'Introduction to HTML',
        description: 'Learn the building blocks of web pages',
        duration: '45 min',
        status: 'completed',
        type: 'lesson'
      },
      {
        id: '2',
        title: 'HTML Quiz',
        description: 'Test your HTML knowledge',
        duration: '15 min',
        status: 'completed',
        type: 'quiz'
      },
      {
        id: '3',
        title: 'CSS Fundamentals',
        description: 'Style your web pages with CSS',
        duration: '1 hour',
        status: 'current',
        type: 'lesson'
      },
      {
        id: '4',
        title: 'CSS Layout & Flexbox',
        description: 'Master modern CSS layouts',
        duration: '1.5 hours',
        status: 'locked',
        type: 'lesson'
      },
      {
        id: '5',
        title: 'Build Your First Webpage',
        description: 'Apply your HTML & CSS skills',
        duration: '2 hours',
        status: 'locked',
        type: 'project'
      },
      {
        id: '6',
        title: 'JavaScript Basics',
        description: 'Add interactivity to your pages',
        duration: '2 hours',
        status: 'locked',
        type: 'lesson'
      }
    ]
  });

  const getStatusIcon = (status: PathItem['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 sm:h-6 sm:w-6 text-green-500" />;
      case 'current':
        return <PlayIcon className="h-5 w-5 sm:h-6 sm:w-6 text-blue-500" />;
      case 'locked':
        return <LockClosedIcon className="h-5 w-5 sm:h-6 sm:w-6 text-gray-400" />;
    }
  };

  const getTypeLabel = (type: PathItem['type']) => {
    switch (type) {
      case 'lesson':
        return <span className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-0.5 rounded">Lesson</span>;
      case 'quiz':
        return <span className="text-xs font-medium text-purple-600 bg-purple-100 px-2 py-0.5 rounded">Quiz</span>;
      case 'project':
        return <span className="text-xs font-medium text-orange-600 bg-orange-100 px-2 py-0.5 rounded">Project</span>;
    }
  };

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Learning Path</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Follow your personalized learning journey</p>
      </div>

      {/* Current Path Overview */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl shadow-lg p-4 sm:p-6 mb-6 sm:mb-8 text-white">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center mb-2">
              <AcademicCapIcon className="h-6 w-6 sm:h-8 sm:w-8 mr-2 sm:mr-3 shrink-0" />
              <h2 className="text-lg sm:text-2xl font-bold">{activePath.title}</h2>
            </div>
            <p className="text-blue-100 text-sm sm:text-base">{activePath.description}</p>
          </div>
          <div className="text-left sm:text-right">
            <div className="text-3xl sm:text-4xl font-bold">{activePath.progress}%</div>
            <p className="text-blue-100 text-sm">Complete</p>
          </div>
        </div>
        <div className="mt-4">
          <div className="w-full bg-blue-800 rounded-full h-2">
            <div
              className="bg-white rounded-full h-2 transition-all duration-300"
              style={{ width: `${activePath.progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Path Items */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-4 sm:p-6 border-b border-gray-200">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900">Course Content</h3>
        </div>

        <div className="divide-y divide-gray-100">
          {activePath.items.map((item, index) => (
            <div
              key={item.id}
              className={`p-4 sm:p-6 ${
                item.status === 'locked' ? 'opacity-60' : ''
              } ${item.status === 'current' ? 'bg-blue-50' : ''}`}
            >
              <div className="flex items-start sm:items-center gap-3 sm:gap-4">
                {/* Timeline connector */}
                <div className="flex flex-col items-center shrink-0">
                  <div className={`w-8 h-8 sm:w-10 sm:h-10 rounded-full flex items-center justify-center ${
                    item.status === 'completed' ? 'bg-green-100' :
                    item.status === 'current' ? 'bg-blue-100' : 'bg-gray-100'
                  }`}>
                    {getStatusIcon(item.status)}
                  </div>
                  {index < activePath.items.length - 1 && (
                    <div className={`w-0.5 h-8 sm:h-12 mt-2 ${
                      item.status === 'completed' ? 'bg-green-300' : 'bg-gray-200'
                    }`} />
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2 mb-1">
                    <h4 className="font-medium text-gray-900 text-sm sm:text-base">{item.title}</h4>
                    {getTypeLabel(item.type)}
                  </div>
                  <p className="text-xs sm:text-sm text-gray-600 mb-2 line-clamp-2">{item.description}</p>
                  <div className="flex items-center text-xs sm:text-sm text-gray-500">
                    <ClockIcon className="h-3.5 w-3.5 sm:h-4 sm:w-4 mr-1" />
                    {item.duration}
                  </div>
                </div>

                {/* Action */}
                <div className="shrink-0">
                  {item.status === 'current' && (
                    <Link
                      href={`/courses/1`}
                      className="bg-blue-600 text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors"
                    >
                      Continue
                    </Link>
                  )}
                  {item.status === 'completed' && (
                    <Link
                      href={`/courses/1`}
                      className="border border-gray-300 text-gray-700 px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium hover:bg-gray-50 transition-colors"
                    >
                      Review
                    </Link>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
