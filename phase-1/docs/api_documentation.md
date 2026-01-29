# API Documentation: Course Companion FTE Phase 1

## Base URL
```
https://your-domain.com/api/v1
```

All endpoints are prefixed with `/api/v1`.

## Authentication
All API requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Content Types
All requests and responses use JSON format with UTF-8 encoding.

## Core Endpoints

### Content Endpoints

#### Get Content Details
```
GET /content/{content_id}
```

Retrieve content metadata and download URL.

**Path Parameters:**
- `content_id` (string, required): UUID of the content item

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Content Title",
  "content_type": "text|video|pdf|image|html|quiz",
  "file_size": 12345,
  "download_url": "https://presigned-url...",
  "content_metadata": "{\"author\": \"John Doe\", \"duration\": 300}",
  "created_at": "2026-01-27T10:00:00Z"
}
```

#### Stream Content
```
GET /content/{content_id}/stream
```

Stream content directly from R2 storage.

**Path Parameters:**
- `content_id` (string, required): UUID of the content item

**Response:**
```json
{
  "content_id": "uuid-string",
  "title": "Content Title",
  "content_type": "text|video|pdf|image|html|quiz",
  "size": 12345,
  "content": "content text or binary data"
}
```

### Course Navigation Endpoints

#### Get Course Structure
```
GET /courses/{course_id}/structure
```

Get the hierarchical structure of a course.

**Path Parameters:**
- `course_id` (string, required): UUID of the course

**Response:**
```json
{
  "course_id": "uuid-string",
  "title": "Course Title",
  "chapters": [
    {
      "chapter_number": 1,
      "title": "Chapter 1",
      "content_items": [
        {
          "id": "content-uuid",
          "title": "Content Title",
          "content_type": "text|video|pdf|image|html|quiz",
          "position": 0,
          "progress_status": "not_started|in_progress|completed"
        }
      ]
    }
  ],
  "total_chapters": 5,
  "total_content_items": 20
}
```

#### Get Next Content
```
GET /courses/{course_id}/next
```

Get the next content item based on user's progress.

**Path Parameters:**
- `course_id` (string, required): UUID of the course

**Response:**
```json
{
  "course_id": "uuid-string",
  "user_id": "uuid-string",
  "has_next_content": true,
  "next_content_id": "uuid-string",
  "next_content_title": "Next Content Title",
  "next_content_type": "text|video|pdf|image|html|quiz",
  "message": "Next content available"
}
```

### Search Endpoints

#### Search Content
```
POST /search
```

Search across course materials using keyword-based search.

**Request Body:**
```json
{
  "query": "search query terms",
  "course_id": "optional course uuid",
  "filters": {
    "content_type": "text|video|pdf|image|html|quiz",
    "created_after": "2026-01-01T00:00:00Z",
    "created_before": "2026-12-31T23:59:59Z"
  },
  "limit": 20,
  "offset": 0
}
```

**Response:**
```json
{
  "query": "search query terms",
  "course_id": "uuid-string",
  "results": [
    {
      "id": "content-uuid",
      "title": "Content Title",
      "content_type": "text|video|pdf|image|html|quiz",
      "course_id": "course-uuid",
      "relevance_score": 0.85,
      "snippet": "relevant text snippet...",
      "created_at": "2026-01-27T10:00:00Z"
    }
  ],
  "total_results": 5,
  "took_ms": 120,
  "message": "Found 5 results in 120ms"
}
```

### Quiz Endpoints

#### Get Quiz
```
GET /quizzes/{quiz_id}
```

Get quiz details and questions.

**Path Parameters:**
- `quiz_id` (string, required): UUID of the quiz

**Response:**
```json
{
  "quiz_id": "uuid-string",
  "title": "Quiz Title",
  "instructions": "Quiz instructions",
  "time_limit_minutes": 30,
  "questions": [
    {
      "question_id": "uuid-string",
      "question_text": "Question text",
      "question_type": "mcq|tf|fill_blank|essay",
      "question_order": 0,
      "points": 5,
      "possible_answers": [
        {
          "answer_id": "uuid-string",
          "answer_text": "Answer text",
          "is_correct": false
        }
      ]
    }
  ]
}
```

#### Submit Quiz
```
POST /quizzes/{quiz_id}/submit
```

Submit quiz answers for grading.

**Path Parameters:**
- `quiz_id` (string, required): UUID of the quiz

**Request Body:**
```json
{
  "user_id": "uuid-string",
  "answers": [
    {
      "question_id": "question-uuid",
      "answer_text": "User's answer text"
    }
  ]
}
```

**Response:**
```json
{
  "quiz_id": "uuid-string",
  "user_id": "uuid-string",
  "overall_score": 85.5,
  "max_score": 100.0,
  "breakdown": [
    {
      "question_id": "question-uuid",
      "question_text": "Question text",
      "user_answer": "User's answer",
      "is_correct": true,
      "points_awarded": 5,
      "feedback": "Feedback text"
    }
  ],
  "detailed_feedback": "Overall feedback",
  "suggested_improvements": ["improvement suggestions"],
  "misconceptions_identified": ["identified misconceptions"],
  "next_learning_recommendations": ["recommendations"],
  "confidence_level": "high|medium|low"
}
```

### Progress Endpoints

#### Update Content Progress
```
PUT /content/{content_id}/progress
```

Update progress for a specific content item.

**Path Parameters:**
- `content_id` (string, required): UUID of the content item

**Request Body:**
```json
{
  "status": "not_started|in_progress|completed",
  "completion_percentage": 75.0,
  "time_spent_seconds": 1200
}
```

**Response:**
```json
{
  "user_id": "uuid-string",
  "content_id": "uuid-string",
  "status": "completed",
  "completion_percentage": 75.0,
  "time_spent_seconds": 1200,
  "updated_at": "2026-01-27T10:00:00Z",
  "message": "Progress updated successfully"
}
```

#### Get User Progress
```
GET /users/{user_id}/progress
```

Get overall progress for a user.

**Path Parameters:**
- `user_id` (string, required): UUID of the user

**Response:**
```json
{
  "user_id": "uuid-string",
  "total_content": 20,
  "completed_content": 15,
  "in_progress_content": 3,
  "not_started_content": 2,
  "overall_completion_percentage": 75.0,
  "current_streak_days": 7,
  "last_active": "2026-01-27T10:00:00Z",
  "progress_distribution": {
    "completed": 15,
    "in_progress": 3,
    "not_started": 2
  }
}
```

### Authentication Endpoints

#### Get User Access Info
```
GET /users/{user_id}/access
```

Get information about user's access to features.

**Path Parameters:**
- `user_id` (string, required): UUID of the user

**Response:**
```json
{
  "user_id": "uuid-string",
  "has_premium_access": true,
  "is_subscription_active": true,
  "subscription_tier": "premium|enterprise|free",
  "subscription_status": "active|inactive|expired|cancelled",
  "access_granted": true,
  "feature_name": "quiz_submission",
  "feature_available": true,
  "message": "Access granted to quiz_submission"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Access denied to the resource
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error occurred

## Rate Limiting

API endpoints implement rate limiting to prevent abuse:
- Standard endpoints: 100 requests per minute per IP
- Premium endpoints: 50 requests per minute per authenticated user
- Upload endpoints: 10 requests per minute per authenticated user

## Premium Feature Access

Access to premium features is controlled by subscription tier:
- Free tier: Basic content access and limited progress tracking
- Premium tier: Adaptive learning, LLM-graded assessments, advanced analytics
- Enterprise tier: All premium features plus custom content and API access

## Security Headers

All responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`