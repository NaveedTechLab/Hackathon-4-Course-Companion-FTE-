# Phase 1 Architecture: Course Companion FTE

## Overview

Phase 1 of the Course Companion FTE implements a digital educational tutor operating 168 hours/week with a deterministic FastAPI backend. The system integrates with OpenAI ChatGPT App via SDK while ensuring zero LLM inference in the backend, following the Zero-Backend-LLM principle.

## Architecture Components

### Backend Services
- **FastAPI Application**: Primary web application framework
- **Database Layer**: Neon PostgreSQL or Supabase for data persistence
- **Content Storage**: Cloudflare R2 for course materials
- **Authentication**: JWT-based user authentication and authorization
- **Premium Access Control**: Subscription-based feature gating

### Core Features
1. **Content Delivery**: Serve educational materials from R2 storage
2. **Navigation**: Chapter sequencing and course progression logic
3. **Grounded Q&A**: Search-based retrieval of relevant sections
4. **Quizzes**: Rule-based grading with answer keys
5. **Progress Tracking**: Completion and streak monitoring
6. **Access Control**: Freemium feature gating

## Data Flow

### Content Request Flow
1. User requests content through API
2. Authentication verified via JWT
3. Premium access checked if required
4. Content metadata retrieved from database
5. R2 client generates presigned URL for content access
6. Content streamed directly from R2 to user

### Quiz Submission Flow
1. User submits quiz answers
2. Authentication and premium access verified
3. Answers validated against answer keys
4. Scores calculated using rule-based system
5. Progress updated in database
6. Results returned with detailed feedback

### Progress Tracking Flow
1. User interacts with content
2. Progress events captured
3. Database updated with current status
4. Streak tracking updated
5. Achievement calculations performed
6. Analytics updated

## Security Architecture

### Access Control
- JWT-based authentication for all API endpoints
- Role-based access control for premium features
- Subscription tier verification for feature access
- Rate limiting to prevent abuse

### Data Isolation
- Premium features separated from core functionality
- Zero LLM calls in backend code
- Deterministic processing for all core features
- Secure R2 access with presigned URLs

### Privacy Protection
- User data encrypted at rest and in transit
- Minimal data collection for functionality
- Compliance with educational privacy standards
- Secure handling of user progress data

## Deployment Architecture

### Infrastructure Components
- **Application Server**: FastAPI application server
- **Database**: Neon PostgreSQL or Supabase instance
- **Object Storage**: Cloudflare R2 for content
- **CDN**: Cloudflare for content delivery acceleration
- **Load Balancer**: Automatic load balancing

### Scalability Considerations
- Horizontal scaling for application servers
- Connection pooling for database efficiency
- Content caching for reduced R2 requests
- Asynchronous processing for heavy operations

## Integration Points

### External APIs
- Cloudflare R2 API for content storage
- Database connection for Neon/Supabase
- OpenAI ChatGPT App SDK for frontend integration

### Internal Services
- Content service for R2 operations
- Quiz service for rule-based grading
- Progress service for tracking and analytics
- Premium service for access control

## Quality Assurance

### Code Quality
- Deterministic algorithms only (no LLM calls in backend)
- Comprehensive unit and integration testing
- Static code analysis for security vulnerabilities
- Performance monitoring and optimization

### Compliance Verification
- Zero-Backend-LLM compliance audit
- Subscription tier enforcement validation
- Data privacy compliance verification
- Security best practices implementation

## Monitoring and Observables

### Performance Metrics
- API response times
- Database query performance
- R2 storage access speeds
- User engagement metrics

### Error Tracking
- API error rates
- Database connection failures
- R2 access errors
- Authentication failures

### Usage Analytics
- Feature usage by subscription tier
- User engagement patterns
- Content consumption metrics
- Progress tracking accuracy