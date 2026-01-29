'use client';

import { useState } from 'react';
import {
  SparklesIcon,
  ArrowsPointingOutIcon,
  LightBulbIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

export default function PremiumFeaturesPage() {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null);

  const premiumFeatures = [
    {
      id: 'adaptive-learning',
      title: 'Adaptive Learning Paths',
      description: 'Personalized learning recommendations based on your progress, strengths, and weaknesses.',
      icon: ArrowsPointingOutIcon,
      benefits: [
        'Tailored content recommendations',
        'Dynamic difficulty adjustment',
        'Gap identification and remediation',
        'Optimized learning pathways'
      ],
      color: 'blue'
    },
    {
      id: 'llm-grading',
      title: 'LLM-Graded Assessments',
      description: 'Detailed feedback on free-form responses with nuanced evaluation by AI.',
      icon: SparklesIcon,
      benefits: [
        'Comprehensive answer evaluation',
        'Constructive feedback and suggestions',
        'Detailed performance insights',
        'Rubric-based grading consistency'
      ],
      color: 'green'
    },
    {
      id: 'synthesis',
      title: 'Cross-Chapter Synthesis',
      description: 'Generate connections across different chapters and concepts for holistic understanding.',
      icon: LightBulbIcon,
      benefits: [
        'Big picture perspective',
        'Inter-concept connections',
        'Synthesis exercises',
        'Overview summaries'
      ],
      color: 'purple'
    }
  ];

  const pricingPlans = [
    {
      name: 'Starter',
      price: '$9.99',
      period: 'month',
      features: [
        'Access to 1 premium feature',
        'Basic adaptive learning',
        'Limited AI assistance',
        'Standard support'
      ],
      popular: false
    },
    {
      name: 'Pro',
      price: '$19.99',
      period: 'month',
      features: [
        'Access to all premium features',
        'Adaptive Learning Paths',
        'LLM-Graded Assessments',
        'Cross-Chapter Synthesis',
        'Priority support'
      ],
      popular: true
    },
    {
      name: 'Enterprise',
      price: '$49.99',
      period: 'month',
      features: [
        'All Pro features',
        'Unlimited usage',
        'Custom AI models',
        'Dedicated account manager',
        'API access',
        'SLA guarantee'
      ],
      popular: false
    }
  ];

  const getColorClasses = (color: string) => {
    switch(color) {
      case 'blue':
        return 'bg-blue-100 text-blue-600';
      case 'green':
        return 'bg-green-100 text-green-600';
      case 'purple':
        return 'bg-purple-100 text-purple-600';
      default:
        return 'bg-gray-100 text-gray-600';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="dashboard-container py-6 sm:py-8 lg:py-12">
        {/* Hero Section */}
        <div className="text-center mb-8 sm:mb-12 lg:mb-16">
          <div className="inline-flex items-center px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 mb-4 sm:mb-6">
            <SparklesIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-1.5 sm:mr-2" />
            <span className="font-semibold text-sm sm:text-base">Premium Features</span>
          </div>
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 sm:mb-6 px-2">
            Unlock Advanced Learning with AI
          </h1>
          <p className="text-sm sm:text-base lg:text-xl text-gray-600 max-w-3xl mx-auto px-4">
            Experience the power of AI-enhanced education with our premium features.
            Personalized learning, intelligent grading, and cross-concept synthesis to accelerate your growth.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 mb-8 sm:mb-12 lg:mb-16">
          {premiumFeatures.map((feature) => (
            <div
              key={feature.id}
              className={`bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6 cursor-pointer transition-all duration-300 hover:shadow-lg ${
                selectedFeature === feature.id ? 'ring-2 ring-blue-500' : ''
              }`}
              onClick={() => setSelectedFeature(feature.id === selectedFeature ? null : feature.id)}
            >
              <div className="flex items-start mb-3 sm:mb-4">
                <div className={`p-2 sm:p-3 rounded-lg ${getColorClasses(feature.color)} shrink-0`}>
                  <feature.icon className="h-5 w-5 sm:h-6 sm:w-6" />
                </div>
                <div className="ml-3 sm:ml-4 flex-1 min-w-0">
                  <h3 className="text-base sm:text-lg font-semibold text-gray-900">{feature.title}</h3>
                  <p className="text-gray-600 text-xs sm:text-sm mt-1">{feature.description}</p>
                </div>
              </div>

              {selectedFeature === feature.id && (
                <div className="mt-3 sm:mt-4 space-y-2 animate-fadeIn">
                  {feature.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center">
                      <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      <span className="text-xs sm:text-sm text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Pricing Section */}
        <div className="mb-8 sm:mb-12 lg:mb-16">
          <div className="text-center mb-6 sm:mb-8 lg:mb-12">
            <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">Choose Your Learning Plan</h2>
            <p className="text-gray-600 text-sm sm:text-base max-w-2xl mx-auto px-4">
              Select the plan that best fits your learning goals and budget. All plans include our core educational features.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
            {pricingPlans.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-xl p-5 sm:p-6 lg:p-8 ${
                  plan.popular
                    ? 'bg-gradient-to-br from-blue-600 to-indigo-700 text-white ring-2 ring-blue-500'
                    : 'bg-white border border-gray-200'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <span className="bg-yellow-400 text-gray-900 px-3 sm:px-4 py-1 rounded-full text-xs sm:text-sm font-semibold whitespace-nowrap">
                      Most Popular
                    </span>
                  </div>
                )}

                <div className="text-center">
                  <h3 className={`text-xl sm:text-2xl font-bold mb-2 ${
                    plan.popular ? 'text-white' : 'text-gray-900'
                  }`}>
                    {plan.name}
                  </h3>
                  <div className="mb-4 sm:mb-6">
                    <span className={`text-3xl sm:text-4xl font-bold ${
                      plan.popular ? 'text-white' : 'text-gray-900'
                    }`}>
                      {plan.price}
                    </span>
                    <span className={`text-base sm:text-lg ${
                      plan.popular ? 'text-blue-200' : 'text-gray-600'
                    }`}>
                      /{plan.period}
                    </span>
                  </div>

                  <ul className="space-y-2 sm:space-y-3 mb-6 sm:mb-8 text-left">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircleIcon className={`h-4 w-4 sm:h-5 sm:w-5 mr-2 mt-0.5 shrink-0 ${
                          plan.popular ? 'text-blue-200' : 'text-green-500'
                        }`} />
                        <span className={`text-xs sm:text-sm ${plan.popular ? 'text-blue-100' : 'text-gray-700'}`}>
                          {feature}
                        </span>
                      </li>
                    ))}
                  </ul>

                  <button
                    className={`w-full py-2.5 sm:py-3 px-4 sm:px-6 rounded-lg text-sm sm:text-base font-semibold transition-colors ${
                      plan.popular
                        ? 'bg-white text-blue-600 hover:bg-gray-100'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {plan.name === 'Pro' ? 'Get Started' : `Choose ${plan.name}`}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* FAQ Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-6 lg:p-8">
          <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-6 sm:mb-8 text-center">Frequently Asked Questions</h2>

          <div className="space-y-4 sm:space-y-6">
            <div className="border-b border-gray-200 pb-4 sm:pb-6">
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">How do premium features enhance learning?</h3>
              <p className="text-gray-600 text-sm sm:text-base">
                Our premium features use AI to provide personalized learning experiences that adapt to your unique
                learning style, pace, and goals. This leads to improved retention and understanding compared to
                traditional learning methods.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-4 sm:pb-6">
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Are premium features available for all courses?</h3>
              <p className="text-gray-600 text-sm sm:text-base">
                Yes, premium features work with all courses in our platform. They enhance your learning experience
                regardless of the subject matter by providing personalized recommendations and feedback.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-4 sm:pb-6">
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Can I cancel my subscription anytime?</h3>
              <p className="text-gray-600 text-sm sm:text-base">
                Absolutely! You can cancel your premium subscription at any time. You&apos;ll continue to have access
                to premium features until the end of your billing period.
              </p>
            </div>

            <div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">How is my data used for personalization?</h3>
              <p className="text-gray-600 text-sm sm:text-base">
                We use your learning data solely to improve your educational experience. Your data is never sold
                to third parties and is kept secure and private in accordance with our privacy policy.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
