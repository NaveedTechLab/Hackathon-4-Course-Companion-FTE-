# Phase 2: Hybrid Intelligence - Technical Specification

## Feature Overview

### Description
Phase 2 implements hybrid intelligence features by integrating the Claude Agent SDK into the existing Course Companion FTE backend. This phase introduces two premium-gated AI-enhanced features: Adaptive Learning Path and LLM-Graded Assessments, while maintaining strict separation from the deterministic Phase 1 logic. All hybrid features are user-initiated, premium-gated, and include cost tracking mechanisms.

### Target Platform
Existing FastAPI backend with Claude Agent SDK integration for enhanced educational features

### Premium Features
1. **Adaptive Learning Path**: Personalized recommendations based on learning data using Claude's reasoning capabilities
2. **LLM-Graded Assessments**: Evaluating free-form answers with detailed feedback using Claude's comprehension abilities

## Core Features

### 1. Adaptive Learning Path (Premium Feature)
**Purpose**: Generate personalized learning recommendations based on user's learning data, performance, and preferences
- Analyze user's progress, strengths, weaknesses, and learning patterns
- Recommend next appropriate content based on knowledge gaps and learning objectives
- Adjust difficulty level based on user's demonstrated understanding
- Suggest alternative pathways when user struggles with concepts

### 2. LLM-Graded Assessments (Premium Feature)
**Purpose**: Evaluate free-form answers with detailed, contextual feedback using LLM comprehension
- Assess open-ended responses that require nuanced understanding
- Provide detailed feedback explaining correctness and suggesting improvements
- Grade essays, explanations, and complex problem-solving steps
- Offer personalized study recommendations based on assessment results

### 3. Cross-Chapter Synthesis (Bonus Feature)
**Purpose**: Generate "big picture" connections across different chapters and concepts
- Identify relationships between concepts taught in different sections
- Create synthesis exercises that combine multiple concepts
- Generate overview summaries connecting disparate topics
- Help users see the interconnected nature of knowledge domains

## Technical Architecture

### System Integration
- Claude Agent SDK integrated into existing FastAPI backend
- Separate API routes isolated from Phase 1 deterministic logic
- Premium gatekeeping middleware to verify user subscription status
- Token cost tracking for each user interaction with hybrid features
- Circuit breaker pattern for LLM service availability

### Data Flow
1. User requests premium feature access
2. System verifies premium subscription status
3. Request is processed by Claude Agent SDK
4. Response is validated and returned to user
5. Token usage is logged for cost tracking

### Security & Isolation
- LLM interactions occur only in designated hybrid endpoints
- No LLM calls in Phase 1 code paths
- All hybrid logic is user-initiated (no auto-triggers)
- Proper authentication and authorization maintained

## API Endpoints

### Adaptive Learning Path Endpoints
```
POST /api/v2/learning-path/personalize
- Headers: Authorization: Bearer {token}
- Request Body:
  {
    "user_id": "uuid",
    "current_progress": {
      "completed_modules": ["module_id1", "module_id2"],
      "performance_scores": {"module_id1": 85, "module_id2": 72},
      "time_spent": {"module_id1": 1200, "module_id2": 1800},
      "learning_preferences": {
        "content_type_preference": "video",
        "difficulty_tolerance": "intermediate",
        "study_time": "evening"
      }
    },
    "learning_objectives": ["objective1", "objective2"],
    "available_content": [
      {
        "id": "content_id",
        "title": "Content Title",
        "type": "video|text|quiz",
        "difficulty": "beginner|intermediate|advanced",
        "prerequisites": ["prereq_id1", "prereq_id2"],
        "tags": ["tag1", "tag2"]
      }
    ]
  }
- Response:
  {
    "recommended_path": [
      {
        "content_id": "uuid",
        "title": "Recommended Content",
        "position": 1,
        "reasoning": "Why this content is recommended",
        "estimated_time": 1500,
        "difficulty_alignment": "matched|challenging|foundational"
      }
    ],
    "alternative_paths": [
      {
        "path_id": "uuid",
        "path_description": "Alternative learning path",
        "contents": ["content_id1", "content_id2"]
      }
    ],
    "focus_areas": [
      {
        "concept": "Concept Name",
        "reason": "Why focus on this concept",
        "recommended_resources": ["resource_id1", "resource_id2"]
      }
    ]
  }
```

### LLM-Graded Assessments Endpoints
```
POST /api/v2/assessments/grade-freeform
- Headers: Authorization: Bearer {token}
- Request Body:
  {
    "assessment_id": "uuid",
    "question": "The original question posed to the user",
    "expected_criteria": [
      {
        "aspect": "Concept Understanding",
        "weight": 0.4,
        "description": "How well the answer demonstrates understanding of core concepts"
      },
      {
        "aspect": "Completeness",
        "weight": 0.3,
        "description": "How thoroughly the answer addresses all parts of the question"
      },
      {
        "aspect": "Clarity",
        "weight": 0.3,
        "description": "How clearly the answer is expressed"
      }
    ],
    "user_response": "The user's free-form response",
    "context": {
      "course_id": "uuid",
      "chapter_context": "Relevant chapter content",
      "user_performance_history": {
        "past_scores": [85, 78, 92],
        "common_mistakes": ["mistake_type1", "mistake_type2"]
      }
    }
  }
- Response:
  {
    "grade": {
      "overall_score": 87,
      "max_score": 100,
      "breakdown": [
        {
          "aspect": "Concept Understanding",
          "score": 85,
          "max_score": 100,
          "feedback": "Shows good understanding of core concepts, minor gaps in application"
        },
        {
          "aspect": "Completeness",
          "score": 90,
          "max_score": 100,
          "feedback": "Addresses all parts of the question comprehensively"
        },
        {
          "aspect": "Clarity",
          "score": 85,
          "max_score": 100,
          "feedback": "Well-structured response, minor clarity issues in the conclusion"
        }
      ]
    },
    "detailed_feedback": "Detailed feedback explaining strengths and areas for improvement",
    "suggested_improvements": [
      "Study section X for better understanding of concept Y",
      "Practice problems related to Z concept"
    ],
    "misconceptions_identified": [
      "Misunderstands concept A as being similar to concept B"
    ],
    "next_learning_recommendations": [
      "Review material on concept X",
      "Practice problems on topic Y"
    ],
    "confidence_level": "high"  // high|medium|low
  }
```

### Cross-Chapter Synthesis Endpoints
```
POST /api/v2/synthesis/connect-concepts
- Headers: Authorization: Bearer {token}
- Request Body:
  {
    "user_id": "uuid",
    "course_id": "uuid",
    "chapters": [
      {
        "chapter_id": "uuid",
        "title": "Chapter Title",
        "key_concepts": ["concept1", "concept2", "concept3"],
        "learning_outcomes": ["outcome1", "outcome2"]
      }
    ],
    "connection_depth": "surface|deep",  // How deep the connections should be
    "output_format": "text|diagram|comparison"  // Preferred output format
  }
- Response:
  {
    "synthesis_report": {
      "connections": [
        {
          "from_chapter": "chapter_id1",
          "to_chapter": "chapter_id2",
          "connection_type": "prerequisite|complementary|analogous",
          "description": "Detailed explanation of the connection",
          "real_world_example": "Example demonstrating the connection",
          "learning_opportunity": "How understanding this connection enhances learning"
        }
      ],
      "big_picture_insights": [
        "Insight 1 about how concepts interrelate",
        "Insight 2 about overarching principles",
        "Insight 3 about applications"
      ],
      "synthesis_diagram": {
        "nodes": [{"id": "concept_id", "label": "Concept Name", "chapter": "chapter_id"}],
        "edges": [{"from": "concept_id1", "to": "concept_id2", "relationship": "relationship_type"}]
      }
    },
    "synthesis_exercises": [
      {
        "exercise_id": "uuid",
        "title": "Synthesis Exercise Title",
        "description": "Exercise description requiring application of multiple concepts",
        "difficulty": "intermediate",
        "estimated_time": 1800
      }
    ]
  }
```

## LLM Prompt Templates

### Adaptive Learning Path Prompt Template
```
INSTRUCTIONS:
You are an expert educational advisor analyzing a student's learning journey to provide personalized recommendations. Based on the student's progress, performance, and preferences, recommend the most appropriate learning path.

CONTEXT ABOUT STUDENT:
- Current progress: {completed_modules}
- Performance scores: {performance_scores}
- Time spent on materials: {time_spent}
- Learning preferences: {learning_preferences}

AVAILABLE LEARNING CONTENT:
{available_content}

STUDENT'S LEARNING OBJECTIVES:
{learning_objectives}

TASK:
1. Identify knowledge gaps based on performance scores and incomplete modules
2. Consider the student's learning preferences and optimal challenge level
3. Recommend the next 3-5 learning modules in priority order
4. For each recommendation, explain why it's appropriate for this specific student
5. Suggest alternative pathways if the student wants to change focus
6. Identify 2-3 focus areas that need attention based on weak performance

RESPONSE FORMAT (as JSON):
{{
  "recommended_path": [
    {{
      "content_id": "...",
      "title": "...",
      "position": 1,
      "reasoning": "...",
      "estimated_time": 1500,
      "difficulty_alignment": "matched|challenging|foundational"
    }}
  ],
  "alternative_paths": [
    {{
      "path_id": "...",
      "path_description": "...",
      "contents": ["...", "..."]
    }}
  ],
  "focus_areas": [
    {{
      "concept": "...",
      "reason": "...",
      "recommended_resources": ["...", "..."]
    }}
  ]
}}
```

### LLM-Graded Assessment Prompt Template
```
INSTRUCTIONS:
You are an expert educator grading a student's free-form response to an assessment question. Evaluate the response based on the provided criteria and provide detailed, constructive feedback.

QUESTION:
{question}

EXPECTED EVALUATION CRITERIA:
{expected_criteria}

STUDENT'S RESPONSE:
{user_response}

CONTEXT:
Course: {course_id}
Chapter Context: {chapter_context}
Student's Performance History: {user_performance_history}

GRADING TASK:
1. Evaluate the response against each criterion, providing specific feedback
2. Assign a score for each criterion (0-100 scale)
3. Provide detailed feedback explaining strengths and areas for improvement
4. Identify any misconceptions in the student's understanding
5. Suggest specific improvements or additional study areas
6. Recommend next learning steps based on this performance

FEEDBACK PRINCIPLES:
- Be specific and constructive
- Reference specific parts of the response when giving feedback
- Acknowledge what was done well
- Provide actionable suggestions for improvement
- Maintain an encouraging tone while being honest about areas needing work

RESPONSE FORMAT (as JSON):
{{
  "grade": {{
    "overall_score": 87,
    "max_score": 100,
    "breakdown": [
      {{
        "aspect": "...",
        "score": 85,
        "max_score": 100,
        "feedback": "..."
      }}
    ]
  }},
  "detailed_feedback": "...",
  "suggested_improvements": ["...", "..."],
  "misconceptions_identified": ["...", "..."],
  "next_learning_recommendations": ["...", "..."],
  "confidence_level": "high"
}}
```

### Cross-Chapter Synthesis Prompt Template
```
INSTRUCTIONS:
You are an expert synthesizer who helps students see connections between different concepts and chapters. Identify meaningful relationships between the provided chapters and concepts.

CHAPTERS AND CONCEPTS:
{chapters}

ANALYSIS TASK:
1. Identify connections between concepts across different chapters
2. Classify each connection as: prerequisite (one builds on another), complementary (work together), or analogous (similar patterns/approaches)
3. Provide real-world examples that demonstrate these connections
4. Explain how understanding these connections enhances overall learning
5. Suggest synthesis exercises that require applying multiple concepts together

CONNECTION TYPES:
- Prerequisite: Understanding concept A is necessary for concept B
- Complementary: Concepts A and B work together to solve complex problems
- Analogous: Concepts A and B share similar patterns or principles despite different applications

RESPONSE FORMAT (as JSON):
{{
  "synthesis_report": {{
    "connections": [
      {{
        "from_chapter": "...",
        "to_chapter": "...",
        "connection_type": "prerequisite|complementary|analogous",
        "description": "...",
        "real_world_example": "...",
        "learning_opportunity": "..."
      }}
    ],
    "big_picture_insights": ["...", "...", "..."],
    "synthesis_diagram": {{
      "nodes": [
        {{"id": "...", "label": "...", "chapter": "..."}}
      ],
      "edges": [
        {{"from": "...", "to": "...", "relationship": "..."}}
      ]
    }}
  }},
  "synthesis_exercises": [
    {{
      "exercise_id": "...",
      "title": "...",
      "description": "...",
      "difficulty": "...",
      "estimated_time": 1800
    }}
  ]
}}
```

## Feature Requirements

### Adaptive Learning Path Requirements
- Must analyze user's historical performance data to identify knowledge gaps
- Should consider learning preferences and optimal challenge level
- Must provide clear reasoning for each recommendation
- Should offer multiple path alternatives
- Must adapt recommendations based on real-time performance
- Should identify focus areas for improvement

### LLM-Graded Assessment Requirements
- Must evaluate free-form responses with nuance beyond keyword matching
- Should provide detailed, constructive feedback
- Must identify specific misconceptions in student understanding
- Should suggest targeted improvement strategies
- Must handle various response lengths and complexities
- Should maintain consistency across different graders

### Cross-Chapter Synthesis Requirements
- Must identify meaningful connections across different learning modules
- Should provide real-world examples of concept connections
- Must suggest practical exercises combining multiple concepts
- Should create visual representations of concept relationships
- Must adapt to different connection depths based on user level

## Justification for LLM Usage

### Why Adaptive Learning Path Requires LLM Reasoning
1. **Complex Pattern Recognition**: Identifying subtle patterns in learning data that indicate knowledge gaps or strengths requires nuanced analysis that goes beyond simple heuristics
2. **Contextual Reasoning**: Balancing multiple factors (performance, time spent, learning preferences) to make personalized recommendations requires sophisticated reasoning
3. **Explanatory Power**: Providing clear, personalized explanations for why certain content is recommended requires natural language understanding and generation
4. **Adaptive Complexity**: Adjusting recommendation difficulty based on nuanced performance patterns requires sophisticated analysis

### Why LLM-Graded Assessments Require LLM Reasoning
1. **Nuanced Evaluation**: Free-form responses often contain partial credit-worthy elements that require understanding of meaning rather than keyword matching
2. **Constructive Feedback**: Providing detailed, personalized feedback that helps students improve requires natural language generation capabilities
3. **Misconception Identification**: Recognizing subtle misunderstandings in complex responses requires deep comprehension
4. **Contextual Assessment**: Evaluating responses in the context of the specific question and learning objectives requires reasoning

### Why Cross-Chapter Synthesis Requires LLM Reasoning
1. **Abstraction and Connection**: Identifying abstract relationships between seemingly disparate concepts requires high-level reasoning
2. **Big Picture Thinking**: Creating holistic views that connect different learning domains requires synthesizing information across contexts
3. **Analogical Reasoning**: Finding similarities between different concepts or approaches requires sophisticated pattern recognition
4. **Explanatory Synthesis**: Articulating how different concepts interrelate in natural language requires understanding and generation capabilities

## User Scenarios & Testing

### Scenario 1: Personalized Learning Path Request
**User**: Premium subscriber seeking optimized learning path
**Flow**:
1. User accesses adaptive learning path feature
2. System verifies premium subscription status
3. User's learning data is analyzed by Claude
4. Personalized path is generated with reasoning
5. User receives recommendations with explanations
**Acceptance Criteria**: Relevant recommendations provided with clear reasoning within 5 seconds

### Scenario 2: Free-Form Assessment Submission
**User**: Premium subscriber submitting an essay question
**Flow**:
1. User submits detailed written response
2. System verifies premium subscription status
3. Response is evaluated by Claude with detailed rubric
4. Detailed feedback with scores and suggestions is returned
5. User receives actionable next steps
**Acceptance Criteria**: Comprehensive feedback provided with specific suggestions within 10 seconds

### Scenario 3: Concept Synthesis Request
**User**: Premium subscriber wanting to understand connections between topics
**Flow**:
1. User requests concept synthesis across chapters
2. System verifies premium subscription status
3. Cross-chapter connections are identified by Claude
4. Synthesis report with connections and exercises is generated
5. User receives visual representation of concept relationships
**Acceptance Criteria**: Meaningful connections identified and presented clearly within 8 seconds

## Functional Requirements

### FR-001: Premium Access Verification
- System SHALL verify user subscription status before executing any hybrid feature
- System SHALL return appropriate error if user lacks premium access
- System SHALL log access attempts for premium features

### FR-002: Adaptive Learning Path Generation
- System SHALL analyze user performance data to identify knowledge gaps
- System SHALL consider learning preferences when making recommendations
- System SHALL provide clear reasoning for each recommendation
- System SHALL offer alternative learning paths when appropriate
- System SHALL update recommendations based on new performance data

### FR-003: LLM Assessment Grading
- System SHALL evaluate free-form responses against detailed rubrics
- System SHALL provide specific, actionable feedback for improvement
- System SHALL identify student misconceptions and learning gaps
- System SHALL maintain consistency in grading standards
- System SHALL provide next-step recommendations based on performance

### FR-004: Cross-Chapter Synthesis
- System SHALL identify meaningful connections across different learning modules
- System SHALL provide real-world examples demonstrating concept connections
- System SHALL generate synthesis exercises combining multiple concepts
- System SHALL create visual representations of concept relationships
- System SHALL adapt synthesis depth to user's level

### FR-005: Token Cost Tracking
- System SHALL track token usage for each user's interaction with hybrid features
- System SHALL log costs by feature type and user ID
- System SHALL provide cost reports for administrative review
- System SHALL implement spending limits if needed
- System SHALL alert when costs exceed thresholds

### FR-006: Error Handling and Fallbacks
- System SHALL gracefully handle Claude API failures
- System SHALL provide fallback recommendations when LLM is unavailable
- System SHALL maintain functionality during service degradation
- System SHALL log all API errors for monitoring
- System SHALL implement circuit breaker pattern for LLM services

## Non-Functional Requirements

### Performance Requirements
- Adaptive learning path generation: < 5 seconds
- Assessment grading: < 10 seconds
- Cross-chapter synthesis: < 8 seconds
- API response time: < 500ms for all endpoints
- System shall handle 100 premium concurrent users with hybrid features

### Scalability Requirements
- System shall scale to accommodate increasing LLM usage
- Token cost monitoring shall handle high-volume usage
- Premium feature access checks shall remain performant at scale
- Caching mechanisms shall reduce redundant LLM calls

### Security Requirements
- User data shall remain private and secure during LLM processing
- All communications with Claude API shall be encrypted
- Token usage tracking shall protect user privacy
- Authentication tokens shall be properly validated

### Reliability Requirements
- System shall maintain 99.5% availability for premium features
- LLM service failures shall not break core functionality
- Token cost tracking shall be accurate and reliable
- Fallback mechanisms shall ensure graceful degradation

## Success Criteria

### Quantitative Measures
- 95% of adaptive learning path requests return within 5 seconds
- 98% of assessment grading requests provide detailed feedback
- 90% of concept synthesis requests identify meaningful connections
- Premium user satisfaction score > 4.5/5.0 for AI features
- Average token cost per interaction stays within budgeted limits

### Qualitative Measures
- Students find personalized recommendations helpful and relevant
- Assessment feedback is perceived as detailed and actionable
- Concept connections help students see bigger picture
- Premium features provide clear value over free offerings
- System maintains trust through transparency about AI use

## Data Schemas

### User Learning Profile Schema
```
UserLearningProfile:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- learning_preferences: JSON (content_type_preference, difficulty_tolerance, study_time)
- performance_history: JSON (scores, timestamps, content_ids)
- knowledge_gaps: JSON (concept_id, severity, last_assessed)
- created_at: timestamp
- updated_at: timestamp
```

### Assessment Result Schema
```
AssessmentResult:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- assessment_id: UUID (foreign key to Assessment)
- llm_grade: JSON (overall_score, breakdown, feedback)
- token_cost: decimal (cost of processing this assessment)
- processing_time_ms: integer
- created_at: timestamp
- updated_at: timestamp
```

### Token Cost Log Schema
```
TokenCostLog:
- id: UUID (primary key)
- user_id: UUID (foreign key to User)
- feature_type: enum (adaptive_learning, assessment_grading, synthesis)
- tokens_used: integer
- cost_usd: decimal
- created_at: timestamp
```

## Implementation Phases

### Phase 2A: Infrastructure Setup
- Set up Claude Agent SDK integration
- Implement premium access verification middleware
- Create token cost tracking infrastructure
- Set up circuit breaker for LLM services

### Phase 2B: Adaptive Learning Path Implementation
- Develop user data analysis algorithms
- Implement Claude integration for path generation
- Create reasoning and explanation capabilities
- Implement alternative path generation

### Phase 2C: LLM Assessment Grading
- Develop rubric-based evaluation system
- Implement Claude integration for grading
- Create feedback generation capabilities
- Implement misconception identification

### Phase 2D: Cross-Chapter Synthesis
- Develop concept connection algorithms
- Implement Claude integration for synthesis
- Create visualization capabilities
- Generate synthesis exercises

### Phase 2E: Integration & Testing
- Integrate all features with existing system
- Conduct performance testing
- Verify cost tracking accuracy
- Test fallback mechanisms

## Risk Assessment

### High-Risk Areas
1. **LLM API Costs**: Unexpectedly high token usage could exceed budget
2. **Response Latency**: LLM processing could slow down user experience
3. **Quality Variance**: LLM responses might vary in quality or accuracy
4. **Privacy Concerns**: Sending user data to LLM services raises privacy issues

### Mitigation Strategies
1. **Cost Management**: Implement usage limits and real-time cost monitoring
2. **Performance**: Implement caching and fallback mechanisms
3. **Quality Control**: Implement quality validation and human oversight
4. **Privacy Protection**: Sanitize data before sending to LLM and use privacy-compliant providers

## Dependencies

### External Dependencies
- Claude Agent SDK
- Anthropic API access
- Existing Phase 1 backend infrastructure
- Database for cost tracking

### Internal Dependencies
- User authentication and authorization system
- Content management system from Phase 1
- Progress tracking system from Phase 1
- Subscription management system