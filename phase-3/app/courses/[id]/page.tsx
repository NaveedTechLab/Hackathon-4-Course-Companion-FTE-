'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { StarIcon, ClockIcon, UserGroupIcon, AcademicCapIcon, PlayCircleIcon, CheckCircleIcon, XCircleIcon, ArrowLeftIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';

// Course data with images
const coursesData: { [key: string]: any } = {
  '1': {
    id: 1,
    title: 'Mathematics Fundamentals',
    description: 'Learn the essential mathematical concepts needed for advanced studies. This comprehensive course covers algebra, geometry, calculus basics, and statistics with hands-on exercises and real-world applications.',
    category: 'mathematics',
    level: 'Beginner',
    duration: '8 weeks',
    rating: 4.8,
    reviews: 124,
    students: 2450,
    instructor: 'Dr. Sarah Johnson',
    instructorBio: 'PhD in Mathematics from MIT with 15 years of teaching experience.',
    price: 99.99,
    thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop',
    progress: 75,
    enrolled: true
  },
  '2': {
    id: 2,
    title: 'Programming Basics',
    description: 'Introduction to programming concepts with Python. Perfect for beginners starting their coding journey. Learn variables, loops, functions, and build your first applications.',
    category: 'programming',
    level: 'Beginner',
    duration: '6 weeks',
    rating: 4.9,
    reviews: 89,
    students: 1876,
    instructor: 'Prof. Michael Chen',
    instructorBio: 'Software Engineer at Google with 10+ years of experience.',
    price: 79.99,
    thumbnail: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&h=400&fit=crop',
    progress: 60,
    enrolled: true
  },
  '3': {
    id: 3,
    title: 'Data Science Essentials',
    description: 'Master the fundamentals of data science and analytics using Python, pandas, and visualization tools. Learn to analyze, visualize, and derive insights from data.',
    category: 'data-science',
    level: 'Intermediate',
    duration: '10 weeks',
    rating: 4.7,
    reviews: 156,
    students: 3210,
    instructor: 'Dr. Emily Rodriguez',
    instructorBio: 'Data Scientist with experience at Netflix and Amazon.',
    price: 129.99,
    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop',
    progress: 0,
    enrolled: false
  },
  '4': {
    id: 4,
    title: 'Machine Learning Foundations',
    description: 'Deep dive into ML algorithms, neural networks, and practical AI applications with hands-on projects. Build real ML models from scratch.',
    category: 'ai',
    level: 'Advanced',
    duration: '12 weeks',
    rating: 4.9,
    reviews: 203,
    students: 1543,
    instructor: 'Dr. James Wilson',
    instructorBio: 'AI Researcher at DeepMind, published 50+ papers.',
    price: 199.99,
    thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop',
    progress: 0,
    enrolled: false
  },
  '5': {
    id: 5,
    title: 'Web Development Bootcamp',
    description: 'Full-stack web development from HTML/CSS to React and Node.js. Build real-world projects and deploy them to production.',
    category: 'web-dev',
    level: 'Intermediate',
    duration: '14 weeks',
    rating: 4.6,
    reviews: 98,
    students: 2876,
    instructor: 'Alex Thompson',
    instructorBio: 'Senior Developer at Shopify, built 100+ websites.',
    price: 149.99,
    thumbnail: 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&h=400&fit=crop',
    progress: 45,
    enrolled: true
  }
};

export default function CourseDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isEnrolling, setIsEnrolling] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      const courseData = coursesData[id as string];
      if (courseData) {
        setCourse({
          ...courseData,
          modules: [
            {
              id: 1,
              title: 'Getting Started',
              duration: '1 week',
              lessons: [
                { id: 1, title: 'Course Introduction', duration: '15 min', completed: true },
                { id: 2, title: 'Setting Up Your Environment', duration: '30 min', completed: true },
                { id: 3, title: 'Core Concepts Overview', duration: '45 min', completed: courseData.progress > 20 },
              ]
            },
            {
              id: 2,
              title: 'Fundamentals',
              duration: '2 weeks',
              lessons: [
                { id: 4, title: 'Basic Principles', duration: '50 min', completed: courseData.progress > 30 },
                { id: 5, title: 'Hands-on Practice', duration: '60 min', completed: courseData.progress > 40 },
                { id: 6, title: 'Common Patterns', duration: '45 min', completed: courseData.progress > 50 },
                { id: 7, title: 'Building Blocks', duration: '55 min', completed: courseData.progress > 60 },
              ]
            },
            {
              id: 3,
              title: 'Advanced Topics',
              duration: '2 weeks',
              lessons: [
                { id: 8, title: 'Advanced Techniques', duration: '65 min', completed: courseData.progress > 70 },
                { id: 9, title: 'Best Practices', duration: '50 min', completed: courseData.progress > 80 },
                { id: 10, title: 'Real-world Applications', duration: '70 min', completed: false },
              ]
            },
            {
              id: 4,
              title: 'Final Project',
              duration: '1 week',
              lessons: [
                { id: 11, title: 'Project Planning', duration: '40 min', completed: false },
                { id: 12, title: 'Implementation', duration: '120 min', completed: false },
                { id: 13, title: 'Review and Submission', duration: '30 min', completed: false },
              ]
            }
          ],
          outcomes: [
            'Master fundamental concepts and principles',
            'Build real-world projects from scratch',
            'Understand industry best practices',
            'Apply knowledge to solve complex problems',
            'Get career-ready skills'
          ],
          prerequisites: [
            'Basic computer literacy',
            'Willingness to learn',
            'Access to a computer with internet'
          ]
        });
      }
      setLoading(false);
    }, 500);
  }, [id]);

  const handleEnroll = async () => {
    setIsEnrolling(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setCourse((prev: any) => ({ ...prev, enrolled: true, progress: 0 }));
    setIsEnrolling(false);
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    for (let i = 0; i < 5; i++) {
      if (i < fullStars) {
        stars.push(<StarIconSolid key={i} className="h-5 w-5 text-yellow-400" />);
      } else {
        stars.push(<StarIcon key={i} className="h-5 w-5 text-gray-300" />);
      }
    }
    return stars;
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-64 bg-gray-200 rounded-xl"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-24 bg-gray-200 rounded-xl"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="dashboard-container">
        <div className="text-center py-12">
          <XCircleIcon className="h-16 w-16 mx-auto text-red-500" />
          <h2 className="text-2xl font-bold text-gray-900 mt-4">Course Not Found</h2>
          <p className="text-gray-600 mt-2">The course you're looking for doesn't exist.</p>
          <Link
            href="/courses"
            className="inline-block mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700"
          >
            Browse Courses
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <Link
          href="/courses"
          className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
        >
          <ArrowLeftIcon className="h-5 w-5 mr-2" />
          Back to Courses
        </Link>
      </div>

      {/* Course Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
        <div className="relative">
          <img
            src={course.thumbnail}
            alt={course.title}
            className="w-full h-64 md:h-80 object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
            <span className={`inline-block px-3 py-1 text-xs font-medium rounded-full mb-3 ${
              course.level === 'Beginner' ? 'bg-green-500' :
              course.level === 'Intermediate' ? 'bg-yellow-500' :
              'bg-red-500'
            }`}>
              {course.level}
            </span>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">{course.title}</h1>
            <p className="text-gray-200">by {course.instructor}</p>
          </div>
        </div>

        <div className="p-6">
          <div className="flex flex-col lg:flex-row lg:justify-between gap-6">
            <div className="flex-1">
              <p className="text-gray-600 text-lg mb-4">{course.description}</p>

              <div className="flex flex-wrap gap-4 mb-4">
                <div className="flex items-center">
                  <div className="flex">{renderStars(course.rating)}</div>
                  <span className="ml-2 font-medium">{course.rating}</span>
                  <span className="text-gray-500 ml-1">({course.reviews} reviews)</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <UserGroupIcon className="h-5 w-5 mr-1" />
                  <span>{course.students.toLocaleString()} students</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <ClockIcon className="h-5 w-5 mr-1" />
                  <span>{course.duration}</span>
                </div>
              </div>

              <p className="text-sm text-gray-500">{course.instructorBio}</p>
            </div>

            <div className="lg:w-80">
              <div className="bg-gray-50 p-6 rounded-xl">
                {course.enrolled ? (
                  <>
                    <div className="text-center mb-4">
                      <p className="text-sm text-gray-600 mb-2">Your Progress</p>
                      <p className="text-3xl font-bold text-blue-600">{course.progress}%</p>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                      <div
                        className="bg-blue-600 h-3 rounded-full transition-all"
                        style={{ width: `${course.progress}%` }}
                      ></div>
                    </div>
                    <button className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                      Continue Learning
                    </button>
                  </>
                ) : (
                  <>
                    <div className="text-center mb-4">
                      <p className="text-3xl font-bold text-gray-900">${course.price}</p>
                      <p className="text-sm text-gray-500">One-time payment</p>
                    </div>
                    <button
                      onClick={handleEnroll}
                      disabled={isEnrolling}
                      className={`w-full px-6 py-3 rounded-lg font-medium transition-colors ${
                        isEnrolling
                          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      {isEnrolling ? 'Enrolling...' : 'Enroll Now'}
                    </button>
                    <p className="text-xs text-gray-500 text-center mt-3">30-day money-back guarantee</p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6">
        {['overview', 'curriculum', 'reviews'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-3 font-medium text-sm capitalize ${
              activeTab === tab
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">What you'll learn</h2>
            <ul className="space-y-3">
              {course.outcomes.map((outcome: string, index: number) => (
                <li key={index} className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
                  <span className="text-gray-700">{outcome}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Requirements</h2>
            <ul className="space-y-3">
              {course.prerequisites.map((req: string, index: number) => (
                <li key={index} className="flex items-start">
                  <AcademicCapIcon className="h-5 w-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
                  <span className="text-gray-700">{req}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'curriculum' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Course Curriculum</h2>

          <div className="space-y-4">
            {course.modules.map((module: any) => (
              <div key={module.id} className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="p-4 bg-gray-50 border-b border-gray-200">
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold text-gray-900">{module.title}</h3>
                    <span className="text-sm text-gray-500">{module.duration}</span>
                  </div>
                </div>

                <div className="divide-y divide-gray-100">
                  {module.lessons.map((lesson: any) => (
                    <div key={lesson.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
                      <div className="flex items-center">
                        {lesson.completed ? (
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                        ) : (
                          <PlayCircleIcon className="h-5 w-5 text-gray-400 mr-3" />
                        )}
                        <div>
                          <div className={`font-medium ${lesson.completed ? 'text-gray-500' : 'text-gray-900'}`}>
                            {lesson.title}
                          </div>
                          <div className="text-sm text-gray-500">{lesson.duration}</div>
                        </div>
                      </div>

                      {course.enrolled && (
                        <button className={`text-sm font-medium ${
                          lesson.completed
                            ? 'text-gray-500 hover:text-gray-700'
                            : 'text-blue-600 hover:text-blue-700'
                        }`}>
                          {lesson.completed ? 'Review' : 'Start'}
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'reviews' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Student Reviews</h2>
            <div className="flex items-center">
              <span className="text-3xl font-bold text-gray-900 mr-2">{course.rating}</span>
              <div className="flex">{renderStars(course.rating)}</div>
            </div>
          </div>

          <div className="space-y-6">
            {[
              { name: 'Ahmad Khan', rating: 5, date: '1 week ago', comment: 'Excellent course! The instructor explains everything clearly. Highly recommended for beginners.' },
              { name: 'Sara Ali', rating: 4, date: '2 weeks ago', comment: 'Very comprehensive content. I learned a lot. Would have liked more practice exercises though.' },
              { name: 'John Smith', rating: 5, date: '3 weeks ago', comment: 'Best course I\'ve taken online. The projects really helped me understand the concepts better.' },
            ].map((review, i) => (
              <div key={i} className="border-b border-gray-100 pb-6 last:border-b-0 last:pb-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                      <span className="text-blue-600 font-medium">{review.name[0]}</span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{review.name}</p>
                      <p className="text-sm text-gray-500">{review.date}</p>
                    </div>
                  </div>
                  <div className="flex">{renderStars(review.rating)}</div>
                </div>
                <p className="text-gray-700 ml-13">{review.comment}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
