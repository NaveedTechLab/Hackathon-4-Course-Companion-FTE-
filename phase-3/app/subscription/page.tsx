'use client';

import { useState } from 'react';
import {
  CheckIcon,
  XMarkIcon,
  SparklesIcon,
  AcademicCapIcon,
  LightBulbIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';

interface PlanFeature {
  name: string;
  free: boolean;
  premium: boolean;
}

export default function SubscriptionPage() {
  const { user } = useAuth();
  const currentPlan = user?.subscription || 'free';
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');

  const features: PlanFeature[] = [
    { name: 'Access to all courses', free: true, premium: true },
    { name: 'Progress tracking', free: true, premium: true },
    { name: 'Basic quizzes', free: true, premium: true },
    { name: 'Adaptive learning paths', free: false, premium: true },
    { name: 'AI-powered assessments', free: false, premium: true },
    { name: 'Cross-chapter synthesis', free: false, premium: true },
    { name: 'Priority support', free: false, premium: true },
    { name: 'Certificates', free: false, premium: true },
    { name: 'Offline access', free: false, premium: true },
    { name: 'Advanced analytics', free: false, premium: true }
  ];

  const premiumFeatures = [
    { icon: LightBulbIcon, title: 'Adaptive Learning', description: 'AI creates personalized study paths' },
    { icon: AcademicCapIcon, title: 'AI Assessments', description: 'Detailed feedback on responses' },
    { icon: ChartBarIcon, title: 'Advanced Analytics', description: 'Deep insights into progress' }
  ];

  return (
    <div className="dashboard-container">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Subscription</h1>
        <p className="text-gray-600 mt-1 text-sm sm:text-base">Manage your plan</p>
      </div>

      {/* Current Plan Banner */}
      {currentPlan === 'premium' && (
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl shadow-lg p-4 sm:p-6 mb-6 sm:mb-8 text-white">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center">
              <SparklesIcon className="h-6 w-6 sm:h-8 sm:w-8 mr-2 sm:mr-3 shrink-0" />
              <div>
                <h2 className="text-lg sm:text-xl font-bold">Premium Member</h2>
                <p className="text-purple-100 text-sm">Access to all premium features</p>
              </div>
            </div>
            <div className="text-left sm:text-right">
              <p className="text-xs sm:text-sm text-purple-100">Next billing</p>
              <p className="font-medium">February 15, 2024</p>
            </div>
          </div>
        </div>
      )}

      {/* Billing Toggle */}
      <div className="flex justify-center mb-6 sm:mb-8">
        <div className="bg-gray-100 p-1 rounded-lg inline-flex">
          <button
            onClick={() => setBillingCycle('monthly')}
            className={`px-4 sm:px-5 py-2 rounded-md text-xs sm:text-sm font-medium transition-colors ${
              billingCycle === 'monthly'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600'
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setBillingCycle('annual')}
            className={`px-4 sm:px-5 py-2 rounded-md text-xs sm:text-sm font-medium transition-colors ${
              billingCycle === 'annual'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600'
            }`}
          >
            Annual <span className="text-green-600 ml-1">-20%</span>
          </button>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8 mb-8 sm:mb-12 max-w-4xl mx-auto">
        {/* Free Plan */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 sm:p-8">
          <div className="mb-5 sm:mb-6">
            <h3 className="text-lg sm:text-xl font-bold text-gray-900">Free</h3>
            <div className="mt-3 sm:mt-4">
              <span className="text-3xl sm:text-4xl font-bold text-gray-900">$0</span>
              <span className="text-gray-500 text-sm sm:text-base">/month</span>
            </div>
            <p className="text-gray-600 mt-2 text-sm">Perfect for getting started</p>
          </div>

          <button
            disabled={currentPlan === 'free'}
            className={`w-full py-2.5 sm:py-3 rounded-lg font-medium text-sm transition-colors ${
              currentPlan === 'free'
                ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            {currentPlan === 'free' ? 'Current Plan' : 'Downgrade'}
          </button>

          <ul className="mt-6 sm:mt-8 space-y-3">
            {features.map((feature) => (
              <li key={feature.name} className="flex items-center text-sm">
                {feature.free ? (
                  <CheckIcon className="h-4 w-4 sm:h-5 sm:w-5 text-green-500 mr-2 sm:mr-3 shrink-0" />
                ) : (
                  <XMarkIcon className="h-4 w-4 sm:h-5 sm:w-5 text-gray-300 mr-2 sm:mr-3 shrink-0" />
                )}
                <span className={feature.free ? 'text-gray-700' : 'text-gray-400'}>
                  {feature.name}
                </span>
              </li>
            ))}
          </ul>
        </div>

        {/* Premium Plan */}
        <div className="bg-white rounded-xl shadow-lg border-2 border-blue-500 p-5 sm:p-8 relative">
          <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
            <span className="bg-blue-500 text-white text-xs font-medium px-3 py-1 rounded-full">
              Popular
            </span>
          </div>

          <div className="mb-5 sm:mb-6">
            <h3 className="text-lg sm:text-xl font-bold text-gray-900">Premium</h3>
            <div className="mt-3 sm:mt-4">
              <span className="text-3xl sm:text-4xl font-bold text-gray-900">
                ${billingCycle === 'monthly' ? '19.99' : '15.99'}
              </span>
              <span className="text-gray-500 text-sm sm:text-base">/month</span>
            </div>
            <p className="text-gray-600 mt-2 text-sm">
              {billingCycle === 'annual' ? 'Billed annually ($191.88/yr)' : 'Billed monthly'}
            </p>
          </div>

          <button
            disabled={currentPlan === 'premium'}
            className={`w-full py-2.5 sm:py-3 rounded-lg font-medium text-sm transition-colors ${
              currentPlan === 'premium'
                ? 'bg-blue-100 text-blue-700 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {currentPlan === 'premium' ? 'Current Plan' : 'Upgrade'}
          </button>

          <ul className="mt-6 sm:mt-8 space-y-3">
            {features.map((feature) => (
              <li key={feature.name} className="flex items-center text-sm">
                <CheckIcon className="h-4 w-4 sm:h-5 sm:w-5 text-green-500 mr-2 sm:mr-3 shrink-0" />
                <span className="text-gray-700">{feature.name}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Premium Features */}
      <div className="bg-gray-50 rounded-xl p-5 sm:p-8 mb-6 sm:mb-8">
        <h3 className="text-lg sm:text-xl font-bold text-gray-900 mb-4 sm:mb-6 text-center">
          Premium Features
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
          {premiumFeatures.map((feature) => (
            <div key={feature.title} className="bg-white p-4 sm:p-6 rounded-lg shadow-sm">
              <div className="h-10 w-10 sm:h-12 sm:w-12 bg-blue-100 rounded-full flex items-center justify-center mb-3 sm:mb-4">
                <feature.icon className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
              </div>
              <h4 className="font-semibold text-gray-900 text-sm sm:text-base mb-1 sm:mb-2">{feature.title}</h4>
              <p className="text-xs sm:text-sm text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Billing Info */}
      {currentPlan === 'premium' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6">
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Billing Information</h3>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6 mb-4 sm:mb-6">
            <div>
              <p className="text-xs sm:text-sm text-gray-600 mb-1">Plan</p>
              <p className="font-medium text-sm sm:text-base">Premium (Monthly)</p>
            </div>
            <div>
              <p className="text-xs sm:text-sm text-gray-600 mb-1">Next Billing</p>
              <p className="font-medium text-sm sm:text-base">Feb 15, 2024</p>
            </div>
            <div>
              <p className="text-xs sm:text-sm text-gray-600 mb-1">Payment</p>
              <p className="font-medium text-sm sm:text-base">Visa ****4242</p>
            </div>
            <div>
              <p className="text-xs sm:text-sm text-gray-600 mb-1">Amount</p>
              <p className="font-medium text-sm sm:text-base">$19.99</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-3 sm:gap-4 pt-4 sm:pt-6 border-t border-gray-200">
            <button className="text-xs sm:text-sm text-blue-600 hover:text-blue-700 font-medium">
              Update Payment
            </button>
            <button className="text-xs sm:text-sm text-gray-600 hover:text-gray-700 font-medium">
              View History
            </button>
            <button className="text-xs sm:text-sm text-red-600 hover:text-red-700 font-medium">
              Cancel Subscription
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
