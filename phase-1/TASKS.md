# Phase 1: Course Companion FTE - Implementation Tasks

## Feature: Course Companion FTE - Phase 1

The Course Companion FTE Phase 1 is a digital educational tutor that operates 168 hours/week, featuring a deterministic FastAPI backend that integrates with OpenAI ChatGPT App via SDK. The system will deliver educational content from Cloudflare R2 storage with no LLM inference in the backend.

## Dependencies
- FastAPI framework and related dependencies
- Database drivers (PostgreSQL)
- Cloudflare R2 SDK
- OpenAI ChatGPT App SDK
- Security libraries (JWT, bcrypt)
- Testing frameworks (pytest, httpx)

## Implementation Strategy
Implement the Course Companion FTE Phase 1 following a phased approach starting with infrastructure setup, followed by core feature development, and concluding with verification and deployment. Focus on deterministic backend operations with zero LLM API calls.

---

## Phase 1: Setup

### Goal
Initialize the FastAPI project and Dockerfile in /phase-1. Configure R2 client and Database connection.

### Independent Test Criteria
- FastAPI application can be started without errors
- Database connection can be established
- R2 client can be initialized
- Docker container builds and runs successfully

### Tasks
- [ ] T001 Create project directory structure in /phase-1
- [ ] T002 Initialize Python project with requirements.txt for FastAPI dependencies
- [ ] T003 Create Dockerfile in /phase-1/Dockerfile
- [ ] T004 Set up environment configuration files in /phase-1/.env
- [ ] T005 Install and configure FastAPI framework in /phase-1/main.py
- [ ] T006 Set up SQLAlchemy ORM with Neon/Supabase database connection in /phase-1/database.py
- [ ] T007 Configure Cloudflare R2 client in /phase-1/storage/r2_client.py
- [ ] T008 Create basic API router structure in /phase-1/api/
- [ ] T009 Set up logging and error handling infrastructure in /phase-1/utils/
- [ ] T010 Create startup script in /phase-1/startup.py

---

## Phase 2: Foundational

### Goal
Implement foundational components including authentication middleware and database models needed for all user stories.

### Independent Test Criteria
- User authentication system works properly
- Database models can be created and queried
- Middleware properly enforces access control
- Database migrations work correctly

### Tasks
- [ ] T011 Create User model in /phase-1/models/user.py
- [ ] T012 Create Course model in /phase-1/models/course.py
- [ ] T013 Create Content model in /phase-1/models/content.py
- [ ] T014 Create Progress model in /phase-1/models/progress.py
- [ ] T015 Create Quiz model in /phase-1/models/quiz.py
- [ ] T016 Create authentication middleware in /phase-1/middleware/auth.py
- [ ] T017 Implement user service in /phase-1/services/user_service.py
- [ ] T018 Set up database migration system with Alembic in /phase-1/migrations/
- [ ] T019 Create base API response models in /phase-1/schemas/
- [ ] T020 Implement subscription verification logic in /phase-1/services/subscription_service.py

---

## Phase 3: [US1] Content Delivery API

### Goal
Implement 'GET /chapters/{id}' and 'GET /chapters/{id}/next' to serve R2 content verbatim.

### Independent Test Criteria
- Can retrieve content from R2 by content ID
- Can navigate to next chapter based on course structure
- Content is served without modification from R2
- Proper authentication and authorization enforced

### Tasks
- [ ] T021 [US1] Create content delivery service in /phase-1/services/content_service.py
- [ ] T022 [US1] Implement GET /api/v1/content/{content_id} endpoint in /phase-1/api/endpoints/content.py
- [ ] T023 [US1] Implement GET /api/v1/content/{content_id}/stream endpoint in /phase-1/api/endpoints/content.py
- [ ] T024 [US1] Create content retrieval logic from R2 in /phase-1/services/content_service.py
- [ ] T025 [US1] Implement chapter navigation logic in /phase-1/services/navigation_service.py
- [ ] T026 [US1] Implement GET /api/v1/courses/{course_id}/next endpoint in /phase-1/api/endpoints/navigation.py
- [ ] T027 [US1] Create content metadata management in /phase-1/services/content_service.py
- [ ] T028 [US1] Add content access controls in /phase-1/middleware/content_access.py
- [ ] T029 [US1] Implement content caching mechanisms in /phase-1/services/content_service.py
- [ ] T030 [US1] Add content access metrics tracking in /phase-1/services/analytics_service.py

---

## Phase 4: [US2] Search API

### Goal
Build a keyword-based Search API for content retrieval.

### Independent Test Criteria
- Search returns relevant content based on keywords
- Results are properly ranked by relevance
- Search respects user permissions and access controls
- Performance meets < 3 second response time requirement

### Tasks
- [ ] T031 [US2] Create search service in /phase-1/services/search_service.py
- [ ] T032 [US2] Implement full-text search across course materials in /phase-1/services/search_service.py
- [ ] T033 [US2] Build search indexing for content in /phase-1/services/index_service.py
- [ ] T034 [US2] Create relevance scoring algorithms in /phase-1/services/search_service.py
- [ ] T035 [US2] Implement citation and reference systems in /phase-1/services/search_service.py
- [ ] T036 [US2] Implement POST /api/v1/search endpoint in /phase-1/api/endpoints/search.py
- [ ] T037 [US2] Add search analytics and logging in /phase-1/services/analytics_service.py
- [ ] T038 [US2] Create search result presentation in /phase-1/schemas/search_schemas.py
- [ ] T039 [US2] Implement faceted search (by type, date, author) in /phase-1/services/search_service.py
- [ ] T040 [US2] Add search access controls in /phase-1/middleware/search_access.py

---

## Phase 5: [US3] Quiz & Progress API

### Goal
Create 'POST /quizzes/submit' for rule-based grading and 'PUT /progress' for streak tracking.

### Independent Test Criteria
- Quiz submissions are graded against answer keys
- Progress is accurately tracked and persisted
- Streak tracking works correctly
- Quiz feedback is immediate and accurate

### Tasks
- [ ] T041 [US3] Create quiz service in /phase-1/services/quiz_service.py
- [ ] T042 [US3] Implement answer key-based grading system in /phase-1/services/quiz_service.py
- [ ] T043 [US3] Create POST /api/v1/quizzes/{quiz_id}/submit endpoint in /phase-1/api/endpoints/quiz.py
- [ ] T044 [US3] Implement quiz result calculation and feedback in /phase-1/services/quiz_service.py
- [ ] T045 [US3] Implement quiz attempt tracking in /phase-1/services/quiz_service.py
- [ ] T046 [US3] Create PUT /api/v1/content/{content_id}/progress endpoint in /phase-1/api/endpoints/progress.py
- [ ] T047 [US3] Implement progress recording mechanisms in /phase-1/services/progress_service.py
- [ ] T048 [US3] Create streak tracking and gamification in /phase-1/services/progress_service.py
- [ ] T049 [US3] Build progress aggregation and reporting in /phase-1/services/progress_service.py
- [ ] T050 [US3] Add quiz statistics and analytics in /phase-1/services/analytics_service.py

---

## Phase 6: [US4] Auth & Access Control

### Goal
Implement access control middleware for the Freemium Gate.

### Independent Test Criteria
- User subscription status is properly verified
- Feature access is enforced based on subscription tier
- Usage tracking works correctly
- Promotional access periods are respected

### Tasks
- [ ] T051 [US4] Implement subscription status verification in /phase-1/services/subscription_service.py
- [ ] T052 [US4] Create feature access control mechanisms in /phase-1/middleware/feature_access.py
- [ ] T053 [US4] Build usage tracking and limitation systems in /phase-1/services/usage_service.py
- [ ] T054 [US4] Implement promotional access controls in /phase-1/services/subscription_service.py
- [ ] T055 [US4] Add access restriction enforcement in /phase-1/middleware/access_control.py
- [ ] T056 [US4] Create GET /api/v1/users/me/access endpoint in /phase-1/api/endpoints/auth.py
- [ ] T057 [US4] Create GET /api/v1/content/{content_id}/access endpoint in /phase-1/api/endpoints/auth.py
- [ ] T058 [US4] Implement access control analytics in /phase-1/services/analytics_service.py
- [ ] T059 [US4] Add free vs premium content boundary enforcement in /phase-1/middleware/content_access.py
- [ ] T060 [US4] Create access control documentation in /phase-1/docs/access-control.md

---

## Phase 7: [US5] Agent Skills

### Goal
Create SKILL.md files for 'concept-explainer', 'quiz-master', 'socratic-tutor', and 'progress-motivator' in the /skills folder.

### Independent Test Criteria
- Each SKILL.md file follows proper format with YAML frontmatter
- Skills define clear capabilities for educational agents
- Skills are properly organized in the /skills directory
- Skills follow best practices for agent behavior

### Tasks
- [ ] T061 [US5] Create /skills directory structure
- [ ] T062 [US5] Create concept-explainer SKILL.md in /skills/concept-explainer/SKILL.md
- [ ] T063 [US5] Create quiz-master SKILL.md in /skills/quiz-master/SKILL.md
- [ ] T064 [US5] Create socratic-tutor SKILL.md in /skills/socratic-tutor/SKILL.md
- [ ] T065 [US5] Create progress-motivator SKILL.md in /skills/progress-motivator/SKILL.md
- [ ] T066 [US5] Add concept-explainer assets in /skills/concept-explainer/assets/
- [ ] T067 [US5] Add quiz-master assets in /skills/quiz-master/assets/
- [ ] T068 [US5] Add socratic-tutor assets in /skills/socratic-tutor/assets/
- [ ] T069 [US5] Add progress-motivator assets in /skills/progress-motivator/assets/
- [ ] T070 [US5] Create skill integration documentation in /skills/README.md

---

## Phase 8: [US6] Verification & Compliance

### Goal
Perform a code audit to ensure ZERO LLM API calls are present in the backend.

### Independent Test Criteria
- No LLM API calls (OpenAI, Anthropic, etc.) found in codebase
- No embedding services or RAG systems in backend
- No agent loops or AI-driven decision making in backend
- All operations are deterministic and rule-based

### Tasks
- [ ] T071 [US6] Create LLM API call detection script in /phase-1/tools/llm_scanner.py
- [ ] T072 [US6] Scan entire codebase for OpenAI API calls in /phase-1/
- [ ] T073 [US6] Scan entire codebase for Anthropic API calls in /phase-1/
- [ ] T074 [US6] Scan entire codebase for other LLM API calls in /phase-1/
- [ ] T075 [US6] Scan for embedding services (OpenAI embeddings, Cohere, etc.) in /phase-1/
- [ ] T076 [US6] Scan for RAG systems or vector databases in /phase-1/
- [ ] T077 [US6] Scan for agent loops or autonomous processes in /phase-1/
- [ ] T078 [US6] Document compliance verification results in /phase-1/compliance-report.md
- [ ] T079 [US6] Validate deterministic behavior across all endpoints in /phase-1/
- [ ] T080 [US6] Create final compliance certificate in /phase-1/final-compliance-cert.md

---

## Dependencies

### User Story Completion Order
1. Setup (T001-T010) → Foundational (T011-T020) → US1 Content Delivery → US2 Search → US3 Quiz/Progress → US4 Auth/Access → US5 Agent Skills → US6 Verification

### Blocking Dependencies
- T011-T020 (Foundational models) must be completed before T021-T080 (Feature tasks)
- T006 (Database connection) required for all model tasks
- T007 (R2 client) required for content delivery tasks
- T016 (Auth middleware) required for access control tasks

---

## Parallel Execution Examples

### Per User Story
- US1: T021, T024, T027 (services) can be developed in parallel with T022, T023, T026 (endpoints)
- US2: T031, T032, T033 (search functionality) can be developed in parallel with T036, T038 (API endpoints)
- US3: T041, T042, T044 (quiz logic) can be developed in parallel with T043, T045 (API endpoints)
- US5: T062-T065 (SKILL.md files) can all be developed in parallel
- US6: T071-T077 (scanning tasks) can be developed in parallel

---

## Implementation Strategy

### MVP First Approach
1. Start with minimal viable implementation of content delivery (US1)
2. Add basic search functionality (US2)
3. Implement quiz and progress tracking (US3)
4. Add access controls (US4)
5. Create agent skills (US5)
6. Perform final verification (US6)

### Incremental Delivery
- Sprint 1: Setup and foundational components (T001-T020)
- Sprint 2: Content delivery and navigation (T021-T030)
- Sprint 3: Search functionality (T031-T040)
- Sprint 4: Quiz and progress systems (T041-T050)
- Sprint 5: Access control (T051-T060)
- Sprint 6: Agent skills (T061-T070)
- Sprint 7: Verification and compliance (T071-T080)