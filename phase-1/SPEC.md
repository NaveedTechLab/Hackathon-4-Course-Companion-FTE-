# Phase 1: Course Companion FTE - Technical Specification

## Feature Overview

### Description
Develop Phase 1 of the Course Companion FTE - a digital educational tutor operating 168 hours/week. This phase implements a deterministic FastAPI backend engine that integrates with OpenAI ChatGPT App via SDK, focusing on core educational features without any LLM API calls in the backend.

### Target Platform
OpenAI ChatGPT App via SDK integration

### Backend Architecture
FastAPI (Python) serving as a deterministic engine with no LLM inference capabilities

## Core Features

### 1. Content Delivery
**Purpose**: Serve educational material from Cloudflare R2 storage
- Retrieve and deliver course content (text, documents, media) from R2 storage
- Support various content types (PDF, DOCX, images, videos, HTML)
- Implement efficient streaming for large files
- Cache frequently accessed content for performance
- Track content access metrics

### 2. Navigation
**Purpose**: Provide logical chapter sequencing and course progression
- Define course structure with chapters, sections, and lessons
- Implement sequential navigation with progress indicators
- Support bookmarking and resume functionality
- Enable course pathway customization
- Track navigation patterns and user progress

### 3. Grounded Q&A
**Purpose**: Provide search-based retrieval of relevant course sections
- Implement full-text search across course materials
- Return precise citations and references to source content
- Support semantic search within document boundaries
- Provide relevance ranking for search results
- Enable context-aware question answering based on available content

### 4. Quizzes
**Purpose**: Deliver rule-based assessment with automated grading
- Create multiple question types (MCQ, true/false, fill-in-blank, essay)
- Implement answer key-based grading with scoring
- Support immediate feedback and explanations
- Enable quiz retakes with different question orders
- Track quiz performance and learning analytics

### 5. Progress Tracking
**Purpose**: Monitor completion rates and learning streaks
- Track course completion percentages
- Monitor learning streaks and consistency
- Record time spent on different materials
- Generate progress reports and insights
- Support gamification elements (badges, achievements)

### 6. Gating & Access Control
**Purpose**: Implement freemium access control mechanisms
- Define free vs premium content boundaries
- Implement user subscription status verification
- Control feature access based on subscription tier
- Support trial periods and promotional access
- Track usage against subscription limits

## Constraints & Requirements

### Strict Constraints
- **No LLM API calls**: Backend must remain completely deterministic
- **No summarization**: No automated content summarization in backend
- **No agent loops**: No AI-driven decision making or autonomous processes
- **Deterministic operations**: All backend operations must be predictable and reproducible
- **File location**: All Phase 1 files must be located in the /phase-1 directory

### Technical Constraints
- Backend: FastAPI (Python 3.9+)
- Content Storage: Cloudflare R2
- Database: Neon PostgreSQL or Supabase
- Target Platform: OpenAI ChatGPT App via SDK
- Authentication: Standard session/token-based system

## User Scenarios & Testing

### Scenario 1: Content Consumption
**User**: Student accessing course materials
**Flow**:
1. User navigates to course content
2. System retrieves content from R2 storage
3. Content is delivered with proper formatting
4. System tracks access for progress metrics
**Acceptance Criteria**: Content loads within 2 seconds, proper error handling for missing content

### Scenario 2: Chapter Navigation
**User**: Student progressing through course
**Flow**:
1. User completes current chapter
2. System unlocks next chapter based on prerequisites
3. Progress is recorded in database
4. Navigation indicators update appropriately
**Acceptance Criteria**: Next chapter unlocks immediately upon completion, progress accurately reflected

### Scenario 3: Question Answering
**User**: Student asking questions about course content
**Flow**:
1. User submits question to system
2. System searches indexed course materials
3. Relevant sections are retrieved and cited
4. Response is delivered with source references
**Acceptance Criteria**: Relevant content returned within 3 seconds, proper citation of sources

### Scenario 4: Quiz Taking
**User**: Student taking an assessment
**Flow**:
1. User starts quiz
2. Questions are presented according to rules
3. Answers are validated against answer keys
4. Results and feedback are provided immediately
**Acceptance Criteria**: Accurate grading against answer keys, immediate feedback provided

### Scenario 5: Progress Tracking
**User**: Student reviewing learning progress
**Flow**:
1. User accesses progress dashboard
2. System aggregates completion data
3. Progress metrics and streaks are displayed
4. Historical data is available for review
**Acceptance Criteria**: Accurate progress calculation, streak tracking works correctly

## Functional Requirements

### FR-001: Content Management
- System SHALL store course materials in Cloudflare R2
- System SHALL provide APIs to upload, retrieve, and delete content
- System SHALL support content metadata (type, size, author, etc.)
- System SHALL implement content versioning
- System SHALL provide content access controls

### FR-002: Navigation Engine
- System SHALL define course structure hierarchies
- System SHALL enforce prerequisite completion for navigation
- System SHALL provide bookmarking functionality
- System SHALL maintain navigation history
- System SHALL support course customization by instructors

### FR-003: Search & Retrieval
- System SHALL index course content for full-text search
- System SHALL return search results with relevance scoring
- System SHALL provide citation information for retrieved content
- System SHALL support faceted search (by type, date, author)
- System SHALL implement search analytics and logging

### FR-004: Assessment Engine
- System SHALL support multiple question types with rule-based grading
- System SHALL validate answers against predefined answer keys
- System SHALL calculate scores automatically
- System SHALL provide immediate feedback and explanations
- System SHALL track quiz attempts and performance

### FR-005: Progress Analytics
- System SHALL track completion percentages for all content
- System SHALL maintain learning streaks and consistency metrics
- System SHALL generate progress reports for users
- System SHALL support progress sharing with instructors
- System SHALL implement progress-based notifications

### FR-006: Access Control
- System SHALL verify user subscription status
- System SHALL enforce feature access based on subscription tier
- System SHALL implement usage tracking against limits
- System SHALL support promotional access periods
- System SHALL provide clear messaging for restricted content

## Non-Functional Requirements

### Performance
- Content delivery: < 2 seconds for files under 10MB
- Search operations: < 3 seconds for typical queries
- API response time: < 500ms for standard operations
- System shall handle 1000 concurrent users

### Scalability
- System shall support horizontal scaling
- Database queries shall be optimized with proper indexing
- Content delivery shall use efficient caching strategies
- System shall handle traffic spikes during peak usage

### Security
- All user data shall be encrypted at rest and in transit
- Authentication tokens shall have appropriate expiration
- Content access shall be properly authorized
- System shall implement rate limiting to prevent abuse

### Reliability
- System shall have 99.9% uptime during operational hours
- Content delivery shall have 99.99% availability
- Database operations shall have proper error handling and recovery
- System shall implement proper logging and monitoring

## Data Schemas

### User Schema
```
User:
- id: UUID (primary key)
- email: string (unique, indexed)
- name: string
- subscription_tier: enum (free, premium, enterprise)
- subscription_status: enum (active, inactive, expired)
- created_at: timestamp
- updated_at: timestamp
- last_active: timestamp
```

### Course Schema
```
Course:
- id: UUID (primary key)
- title: string
- description: text
- creator_id: UUID (foreign key to User)
- status: enum (draft, published, archived)
- created_at: timestamp
- updated_at: timestamp
- enrollment_count: integer
```

### Content Schema
```
Content:
- id: UUID (primary key)
- course_id: UUID (foreign key to Course)
- title: string
- content_type: enum (text, video, pdf, image, html, quiz)
- r2_key: string (reference to R2 storage)
- file_size: integer
- content_metadata: JSON (author, duration, etc.)
- created_at: timestamp
- updated_at: timestamp
```

### Progress Schema
```
Progress:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- content_id: UUID (foreign key to Content)
- status: enum (not_started, in_progress, completed)
- completion_percentage: decimal (0.00 to 100.00)
- time_spent_seconds: integer
- last_accessed: timestamp
- created_at: timestamp
- updated_at: timestamp
```

### Quiz Schema
```
Quiz:
- id: UUID (primary key)
- content_id: UUID (foreign key to Content)
- title: string
- instructions: text
- time_limit_minutes: integer
- max_attempts: integer
- created_at: timestamp
- updated_at: timestamp

QuizQuestion:
- id: UUID (primary key)
- quiz_id: UUID (foreign key to Quiz)
- question_text: text
- question_type: enum (mcq, tf, fill_blank, essay)
- question_order: integer
- points: integer
- created_at: timestamp

QuizAnswer:
- id: UUID (primary key)
- question_id: UUID (foreign key to QuizQuestion)
- answer_text: text
- is_correct: boolean
- points_awarded: integer
- created_at: timestamp
```

## API Endpoints

### Content Delivery API
```
GET /api/v1/content/{content_id}
- Retrieve content metadata and download URL
- Requires authentication
- Returns: Content details with signed R2 URL

GET /api/v1/content/{content_id}/stream
- Stream content directly from R2
- Requires authentication and authorization
- Returns: Content stream with proper headers
```

### Navigation API
```
GET /api/v1/courses/{course_id}/structure
- Get course structure with chapter/section hierarchy
- Returns: Nested structure of course content

GET /api/v1/courses/{course_id}/next
- Get next available content based on progress
- Returns: Next content item or null if course complete

POST /api/v1/content/{content_id}/bookmark
- Set bookmark for current user
- Body: {position: integer, note: string}
- Returns: Bookmark confirmation
```

### Search API
```
POST /api/v1/search
- Search across course content
- Body: {query: string, course_id: UUID, filters: object}
- Returns: Search results with citations

POST /api/v1/search/autocomplete
- Get search suggestions
- Body: {query: string}
- Returns: Suggested completions
```

### Quiz API
```
GET /api/v1/quizzes/{quiz_id}
- Get quiz details and questions
- Returns: Quiz with questions and metadata

POST /api/v1/quizzes/{quiz_id}/submit
- Submit quiz answers for grading
- Body: {answers: array of {question_id, answer_text}}
- Returns: Grading results and feedback

GET /api/v1/quizzes/{quiz_id}/results
- Get quiz results for user
- Returns: Score, feedback, and attempt history
```

### Progress API
```
GET /api/v1/users/me/progress
- Get current user's progress summary
- Returns: Overall progress and streaks

GET /api/v1/courses/{course_id}/progress
- Get progress for specific course
- Returns: Detailed progress breakdown

POST /api/v1/content/{content_id}/progress
- Update progress for content item
- Body: {status: string, completion_percentage: number}
- Returns: Updated progress
```

### Access Control API
```
GET /api/v1/users/me/access
- Get current user's access level and features
- Returns: Subscription status and feature access

GET /api/v1/content/{content_id}/access
- Check access to specific content
- Returns: Access status and requirements
```

## Success Criteria

### Quantitative Measures
- 95% of content requests served with < 2 second response time
- 99.9% uptime maintained during operational hours
- System supports 1000+ concurrent users without performance degradation
- 99% of quiz grading completed with 100% accuracy against answer keys
- Search returns relevant results within 3 seconds for 95% of queries

### Qualitative Measures
- Students can seamlessly access and consume course materials
- Navigation flow feels intuitive and guides learning progression
- Q&A system provides accurate and helpful responses based on available content
- Quiz feedback is immediate and educational
- Progress tracking motivates continued learning
- Access controls are transparent and fair to users

### User Experience Goals
- Students spend 80%+ of their study time engaged with content
- Course completion rates improve by 30% compared to traditional methods
- User satisfaction scores exceed 4.0/5.0 for core features
- Students return to the platform daily during active courses

## Assumptions

### Technical Assumptions
- Cloudflare R2 provides reliable content storage with appropriate access controls
- FastAPI can handle the expected load requirements for the educational platform
- Database performance can be optimized through proper indexing and query optimization
- OpenAI ChatGPT App SDK provides stable integration points for the platform

### Business Assumptions
- Students will engage with content delivered through the ChatGPT interface
- Freemium model will drive conversion to premium subscriptions
- Rule-based assessment is sufficient for Phase 1 without AI grading
- Content creators will provide properly structured materials for search functionality

### Operational Assumptions
- Content is pre-processed and properly formatted before upload to R2
- Instructors will maintain answer keys for all assessment content
- Students have adequate internet connectivity for content consumption
- User authentication and authorization are handled through standard mechanisms

## Dependencies

### External Dependencies
- Cloudflare R2 for content storage
- Neon PostgreSQL or Supabase for data persistence
- OpenAI ChatGPT App SDK for platform integration
- Standard Python libraries for FastAPI and related functionality

### Internal Dependencies
- Proper content preparation and upload processes
- Instructors providing well-structured course materials
- Students having appropriate devices and connectivity
- Content creators following established formatting guidelines

## Edge Cases & Error Conditions

### Content Delivery Errors
- Missing content in R2 storage
- Network interruptions during streaming
- Unauthorized access attempts
- R2 service unavailability

### Navigation Edge Cases
- User skipping prerequisite content
- Course structure modifications during user progress
- Concurrent modifications to course structure
- Invalid navigation states

### Search Edge Cases
- No results found for queries
- Extremely broad or narrow search queries
- Search index inconsistencies
- Malformed search queries

### Quiz Edge Cases
- Multiple simultaneous quiz attempts
- Network interruptions during quiz taking
- Invalid answer submissions
- Timer synchronization issues

### Progress Tracking Edge Cases
- Concurrent progress updates
- System failures during progress saving
- User account changes during progress
- Content removal affecting progress calculations

## Implementation Phases

### Phase 1A: Core Infrastructure
- Set up FastAPI backend with database integration
- Implement basic user authentication and authorization
- Create content storage and retrieval mechanisms
- Establish API endpoint foundations

### Phase 1B: Feature Implementation
- Develop content delivery and streaming capabilities
- Implement navigation and course structure
- Create search and retrieval functionality
- Build quiz engine with rule-based grading

### Phase 1C: Integration & Polish
- Integrate with OpenAI ChatGPT App
- Implement progress tracking and analytics
- Add access control and freemium features
- Complete error handling and edge case management

## Performance Benchmarks

### Baseline Metrics
- Content delivery: Target < 2 seconds for files up to 10MB
- API response time: Target < 500ms for 95% of requests
- Search performance: Target < 3 seconds for complex queries
- System throughput: Target 1000+ concurrent users

### Monitoring Requirements
- Real-time performance dashboards
- Automated alerting for performance degradation
- User experience tracking and feedback collection
- Regular performance benchmarking and optimization