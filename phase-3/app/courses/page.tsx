'use client';

import { useState, useEffect } from 'react';
import { StarIcon, ClockIcon, UserGroupIcon, AcademicCapIcon, MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import Link from 'next/link';

interface Course {
  id: number;
  title: string;
  description: string;
  category: string;
  level: string;
  duration: string;
  rating: number;
  reviews: number;
  students: number;
  instructor: string;
  thumbnail: string;
  progress: number;
  enrolled: boolean;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [enrollingId, setEnrollingId] = useState<number | null>(null);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setCourses([
        {
          id: 1,
          title: 'Mathematics Fundamentals',
          description: 'Learn the essential mathematical concepts needed for advanced studies including algebra, calculus, and statistics.',
          category: 'mathematics',
          level: 'Beginner',
          duration: '8 weeks',
          rating: 4.8,
          reviews: 124,
          students: 2450,
          instructor: 'Dr. Sarah Johnson',
          thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=250&fit=crop',
          progress: 75,
          enrolled: true
        },
        {
          id: 2,
          title: 'Programming Basics',
          description: 'Introduction to programming concepts with Python. Perfect for beginners starting their coding journey.',
          category: 'programming',
          level: 'Beginner',
          duration: '6 weeks',
          rating: 4.9,
          reviews: 89,
          students: 1876,
          instructor: 'Prof. Michael Chen',
          thumbnail: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400&h=250&fit=crop',
          progress: 60,
          enrolled: true
        },
        {
          id: 3,
          title: 'Data Science Essentials',
          description: 'Master the fundamentals of data science and analytics using Python, pandas, and visualization tools.',
          category: 'data-science',
          level: 'Intermediate',
          duration: '10 weeks',
          rating: 4.7,
          reviews: 156,
          students: 3210,
          instructor: 'Dr. Emily Rodriguez',
          thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop',
          progress: 0,
          enrolled: false
        },
        {
          id: 4,
          title: 'Machine Learning Foundations',
          description: 'Deep dive into ML algorithms, neural networks, and practical AI applications with hands-on projects.',
          category: 'ai',
          level: 'Advanced',
          duration: '12 weeks',
          rating: 4.9,
          reviews: 203,
          students: 1543,
          instructor: 'Dr. James Wilson',
          thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop',
          progress: 0,
          enrolled: false
        },
        {
          id: 5,
          title: 'Web Development Bootcamp',
          description: 'Full-stack web development from HTML/CSS to React and Node.js. Build real-world projects.',
          category: 'web-dev',
          level: 'Intermediate',
          duration: '14 weeks',
          rating: 4.6,
          reviews: 98,
          students: 2876,
          instructor: 'Alex Thompson',
          thumbnail: 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=250&fit=crop',
          progress: 45,
          enrolled: true
        },
        {
          id: 6,
          title: 'Cybersecurity Fundamentals',
          description: 'Essential concepts for protecting digital assets, network security, and ethical hacking basics.',
          category: 'security',
          level: 'Intermediate',
          duration: '9 weeks',
          rating: 4.8,
          reviews: 76,
          students: 1345,
          instructor: 'Dr. Lisa Park',
          thumbnail: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=250&fit=crop',
          progress: 0,
          enrolled: false
        },
        {
          id: 7,
          title: 'UI/UX Design Principles',
          description: 'Learn design thinking, user research, wireframing, and create beautiful interfaces with Figma.',
          category: 'design',
          level: 'Beginner',
          duration: '8 weeks',
          rating: 4.7,
          reviews: 134,
          students: 1987,
          instructor: 'Maria Garcia',
          thumbnail: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&h=250&fit=crop',
          progress: 0,
          enrolled: false
        },
        {
          id: 8,
          title: 'Cloud Computing with AWS',
          description: 'Master Amazon Web Services, deploy applications, and learn cloud architecture best practices.',
          category: 'cloud',
          level: 'Advanced',
          duration: '10 weeks',
          rating: 4.8,
          reviews: 167,
          students: 2234,
          instructor: 'David Kim',
          thumbnail: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=250&fit=crop',
          progress: 0,
          enrolled: false
        }
      ]);
      setLoading(false);
    }, 500);
  }, []);

  const categories = [
    { id: 'all', name: 'All' },
    { id: 'mathematics', name: 'Math' },
    { id: 'programming', name: 'Programming' },
    { id: 'data-science', name: 'Data Science' },
    { id: 'ai', name: 'AI & ML' },
    { id: 'web-dev', name: 'Web Dev' },
    { id: 'security', name: 'Security' },
    { id: 'design', name: 'Design' },
    { id: 'cloud', name: 'Cloud' }
  ];

  const filteredCourses = courses.filter(course => {
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory;
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.instructor.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const enrollCourse = async (courseId: number) => {
    setEnrollingId(courseId);
    await new Promise(resolve => setTimeout(resolve, 800));
    setCourses(prev => prev.map(course =>
      course.id === courseId ? { ...course, enrolled: true, progress: 0 } : course
    ));
    setEnrollingId(null);
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    for (let i = 0; i < 5; i++) {
      if (i < fullStars) {
        stars.push(<StarIconSolid key={i} className="h-3.5 w-3.5 sm:h-4 sm:w-4 text-yellow-400" />);
      } else {
        stars.push(<StarIcon key={i} className="h-3.5 w-3.5 sm:h-4 sm:w-4 text-gray-300" />);
      }
    }
    return stars;
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-12 bg-gray-200 rounded w-full"></div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="bg-white rounded-xl shadow-sm overflow-hidden">
                <div className="h-40 sm:h-48 bg-gray-200" />
                <div className="p-4 sm:p-5 space-y-3">
                  <div className="h-5 bg-gray-200 rounded w-3/4" />
                  <div className="h-4 bg-gray-200 rounded w-full" />
                  <div className="h-4 bg-gray-200 rounded w-2/3" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Browse Courses</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Discover courses that match your learning goals</p>
      </div>

      {/* Search and Filters */}
      <div className="mb-6 space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search courses..."
              className="w-full pl-10 pr-4 py-2.5 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="lg:hidden px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
          >
            <FunnelIcon className="h-5 w-5 text-gray-500" />
            <span className="hidden sm:inline text-sm">Filters</span>
          </button>
        </div>

        {/* Category Filters - Desktop */}
        <div className="hidden lg:flex gap-2 flex-wrap">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === category.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Category Filters - Mobile */}
        {showFilters && (
          <div className="lg:hidden flex gap-2 flex-wrap p-4 bg-white rounded-lg border border-gray-200">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => {
                  setSelectedCategory(category.id);
                  setShowFilters(false);
                }}
                className={`px-3 py-1.5 rounded-full text-xs sm:text-sm font-medium transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Results count */}
      <p className="text-xs sm:text-sm text-gray-600 mb-4">
        {filteredCourses.length} {filteredCourses.length === 1 ? 'course' : 'courses'} found
        {searchQuery && ` for "${searchQuery}"`}
      </p>

      {/* Course Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        {filteredCourses.map((course) => (
          <div key={course.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow group">
            <div className="relative overflow-hidden">
              <img
                src={course.thumbnail}
                alt={course.title}
                className="w-full h-40 sm:h-48 object-cover group-hover:scale-105 transition-transform duration-300"
              />
              {course.enrolled && (
                <div className="absolute top-2 left-2 sm:top-3 sm:left-3 bg-green-500 text-white text-xs font-medium px-2 py-0.5 sm:py-1 rounded">
                  Enrolled
                </div>
              )}
              <div className="absolute top-2 right-2 sm:top-3 sm:right-3">
                <span className={`px-2 py-0.5 sm:py-1 text-xs font-medium rounded ${
                  course.level === 'Beginner' ? 'bg-green-100 text-green-800' :
                  course.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {course.level}
                </span>
              </div>
            </div>

            <div className="p-4 sm:p-5">
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-1.5 sm:mb-2 line-clamp-1">{course.title}</h3>
              <p className="text-gray-600 text-xs sm:text-sm mb-3 line-clamp-2">{course.description}</p>

              <div className="flex items-center text-xs sm:text-sm text-gray-500 mb-2 sm:mb-3">
                <UserGroupIcon className="h-3.5 w-3.5 sm:h-4 sm:w-4 mr-1" />
                <span>{(course.students / 1000).toFixed(1)}k</span>
                <span className="mx-2">•</span>
                <ClockIcon className="h-3.5 w-3.5 sm:h-4 sm:w-4 mr-1" />
                <span>{course.duration}</span>
              </div>

              <div className="flex items-center mb-3 sm:mb-4">
                <div className="flex items-center">{renderStars(course.rating)}</div>
                <span className="text-xs sm:text-sm font-medium ml-1.5">{course.rating}</span>
                <span className="text-gray-400 text-xs sm:text-sm mx-1">•</span>
                <span className="text-gray-500 text-xs sm:text-sm">({course.reviews})</span>
              </div>

              {course.enrolled && (
                <div className="mb-3 sm:mb-4">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-medium text-blue-600">{course.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-blue-600 h-1.5 rounded-full"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>
              )}

              <div className="flex justify-between items-center pt-3 sm:pt-4 border-t border-gray-100">
                <span className="text-xs sm:text-sm text-gray-600 truncate mr-2">by {course.instructor}</span>

                {course.enrolled ? (
                  <Link
                    href={`/courses/${course.id}`}
                    className="bg-blue-600 text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium hover:bg-blue-700 transition-colors shrink-0"
                  >
                    Continue
                  </Link>
                ) : (
                  <button
                    onClick={() => enrollCourse(course.id)}
                    disabled={enrollingId === course.id}
                    className={`px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors shrink-0 ${
                      enrollingId === course.id
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {enrollingId === course.id ? 'Enrolling...' : 'Enroll'}
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCourses.length === 0 && (
        <div className="text-center py-12">
          <AcademicCapIcon className="h-12 w-12 sm:h-16 sm:w-16 mx-auto text-gray-400" />
          <h3 className="text-base sm:text-lg font-medium text-gray-900 mt-4 mb-2">No courses found</h3>
          <p className="text-sm text-gray-600 mb-4">Try adjusting your search or filters</p>
          <button
            onClick={() => { setSearchQuery(''); setSelectedCategory('all'); }}
            className="text-blue-600 hover:text-blue-700 font-medium text-sm"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}
