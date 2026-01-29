# Phase 2: Hybrid Intelligence Implementation

This directory contains the implementation for Phase 2 of the Course Companion FTE - Hybrid Intelligence features. This phase integrates Claude Agent SDK to provide premium AI-enhanced educational features while maintaining separation from deterministic Phase 1 logic.

## Features

### 1. Adaptive Learning Path (Premium)
Personalized learning recommendations using OpenRouter/OpenAI's reasoning capabilities to analyze user performance and suggest optimal learning paths.

### 2. LLM-Graded Assessments (Premium)
Evaluation of free-form answers with detailed feedback using OpenRouter/OpenAI's comprehension abilities.

### 3. Cross-Chapter Synthesis (Bonus)
Generation of "big picture" connections across different chapters and concepts.

### 4. Cloudflare R2 Content Storage
Secure and scalable content storage using Cloudflare R2 with:
- File upload and download capabilities
- Content management and metadata tracking
- Presigned URL generation for secure access
- Bulk operations and file listings

## Architecture

### Technical Stack
- **Backend**: FastAPI (continuing from Phase 1)
- **LLM Integration**: OpenAI Agent SDK
- **Database**: PostgreSQL (Neon/Supabase) - continuing from Phase 1
- **Content Storage**: Cloudflare R2 - continuing from Phase 1
- **Authentication**: JWT-based - continuing from Phase 1

### System Design
- Hybrid endpoints isolated from Phase 1 deterministic logic
- Premium access control middleware
- Token cost tracking for each user interaction
- Circuit breaker pattern for LLM service availability
- Fallback mechanisms for service degradation

## API Endpoints

### Adaptive Learning Path
- `POST /api/v2/premium/adaptive-learning/generate` - Generate personalized learning recommendations
- `POST /api/v2/premium/adaptive-learning/recommendations` - Get learning recommendations

### LLM-Graded Assessments
- `POST /api/v2/premium/assessments/grade-freeform` - Grade free-form responses with detailed feedback
- `POST /api/v2/premium/assessments/grade-essay` - Grade essay questions
- `POST /api/v2/premium/assessments/grade-problem-solving` - Grade problem-solving responses
- `GET /api/v2/premium/assessments/statistics/{user_id}` - Get grading statistics

### Cross-Chapter Synthesis
- `POST /api/v2/premium/synthesis/synthesize` - Generate cross-chapter synthesis
- `POST /api/v2/premium/synthesis/overview` - Generate course overview summary
- `POST /api/v2/premium/synthesis/exercise` - Generate synthesis exercises
- `GET /api/v2/premium/synthesis/recommendations/{course_id}` - Get synthesis recommendations

## Security & Compliance

### Premium Access Control
- All hybrid features require premium subscription verification
- Role-based access control for feature availability
- Usage tracking for premium features

### Data Privacy
- Minimal user data sent to LLM services
- Data sanitization before LLM processing
- Compliance with educational privacy regulations

### Cost Management
- Token usage tracking per user
- Spending limits and alerts
- Budget monitoring dashboard

## Implementation Status
- [x] Claude Agent SDK integration
- [x] Premium access control middleware
- [x] Adaptive learning path implementation
- [x] LLM-graded assessments implementation
- [x] Cross-chapter synthesis implementation
- [x] Token cost tracking system
- [x] Fallback mechanisms
- [x] Performance optimization
- [x] Security hardening
- [x] Testing and validation

## Getting Started

1. Ensure Phase 1 backend is running
2. Obtain OpenRouter API credentials (or OpenAI API credentials as alternative)
3. Configure Cloudflare R2 for content storage
4. Configure environment variables:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   LLM_MODEL=openai/gpt-3.5-turbo

   # OR for OpenAI directly:
   # OPENAI_API_KEY=your_openai_api_key

   # Database configuration
   DATABASE_URL=your_postgresql_connection_string

   # Cloudflare R2 configuration
   CLOUDFLARE_ACCOUNT_ID=your_account_id
   CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key
   CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_key
   CLOUDFLARE_R2_BUCKET_NAME=course-companion-fte

   # Application configuration
   SECRET_KEY=your_secret_key
   PREMIUM_TIER_COST_PER_THOUSAND_TOKENS=0.015  # Example cost
   ```
5. Run Phase 2 services alongside Phase 1

## Performance Benchmarks
- Adaptive learning path generation: < 5 seconds
- Assessment grading: < 10 seconds
- Cross-chapter synthesis: < 8 seconds
- Token cost per interaction: Within budgeted limits

## Monitoring & Observability
- Token usage tracking by user and feature
- API response time monitoring
- Error rate tracking
- Premium feature adoption metrics