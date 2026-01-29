# Phase 3: Web App Implementation Tasks

## Feature: Course Companion FTE - Phase 3 Web App

The Course Companion FTE Phase 3 is a full standalone Web App using Next.js/React that consolidates all Phase 1 (deterministic) and Phase 2 (hybrid) features into a unified educational platform. The system maintains Zero-Backend-LLM as the default for core features while exposing premium AI-enhanced capabilities through a single consolidated API.

## Dependencies
- Next.js framework and related dependencies
- React libraries for educational components
- Tailwind CSS for responsive design
- UI libraries for dashboard components (Chart.js, etc.)
- Database connection libraries (PostgreSQL)
- Claude Agent SDK for premium features
- Cloudflare R2 client for content storage
- Authentication and authorization libraries

## Implementation Strategy
Implement the Course Companion FTE Phase 3 following a phased approach starting with frontend setup, followed by backend consolidation, then UI development, feature integration, and finally quality assurance. Focus on creating a responsive LMS dashboard that integrates both deterministic and hybrid intelligence features while maintaining proper access controls.

---

## Phase 1: Setup

### Goal
Initialize the Next.js project structure in /phase-3 with Tailwind CSS for responsive design.

### Independent Test Criteria
- Next.js project is properly initialized with correct directory structure
- Tailwind CSS is configured and working
- Basic development server runs without errors
- Responsive design framework is functional

### Tasks
- [ ] T001 Create project directory structure in /phase-3
- [ ] T002 Initialize Next.js project with TypeScript in /phase-3
- [ ] T003 Configure Tailwind CSS for responsive design in /phase-3
- [ ] T004 Set up project configuration files (package.json, tsconfig.json, next.config.js) in /phase-3
- [ ] T005 Create basic layout structure in /phase-3/app/layout.tsx
- [ ] T006 Set up environment configuration in /phase-3/.env.local
- [ ] T007 Create basic page structure in /phase-3/app/page.tsx
- [ ] T008 Configure ESLint and Prettier in /phase-3
- [ ] T009 Set up basic API route structure in /phase-3/app/api/
- [ ] T010 Create initial directory structure for components in /phase-3/components/

## Phase 2: Foundational

### Goal
Implement foundational components including the consolidated backend API and basic UI framework.

### Independent Test Criteria
- Single API interface successfully consolidates Phase 1 and Phase 2 routes
- Basic UI framework is established with responsive components
- Authentication and authorization systems are in place
- Database connections are properly configured

### Tasks
- [ ] T011 Set up consolidated FastAPI backend in /phase-3/backend/
- [ ] T012 Create API router to consolidate Phase 1 and Phase 2 routes in /phase-3/backend/api/router.py
- [ ] T013 Implement authentication middleware in /phase-3/backend/middleware/auth.py
- [ ] T014 Create database models for consolidated backend in /phase-3/backend/models/
- [ ] T015 Set up database connection in /phase-3/backend/database.py
- [ ] T016 Create base component library in /phase-3/components/ui/
- [ ] T017 Implement responsive layout components in /phase-3/components/layout/
- [ ] T018 Create API service layer in /phase-3/lib/api.ts
- [ ] T019 Set up state management system in /phase-3/store/
- [ ] T020 Create utility functions for the application in /phase-3/lib/utils.ts

## Phase 3: [US1] Dashboard UI

### Goal
Build the course sidebar (navigation) and main content window for the LMS dashboard.

### Independent Test Criteria
- Course sidebar displays course structure and navigation elements
- Main content window properly renders different content types
- Navigation between course sections works smoothly
- Responsive design works across device sizes

### Tasks
- [ ] T021 [US1] Create course navigation sidebar component in /phase-3/components/dashboard/CourseSidebar.tsx
- [ ] T022 [US1] Implement chapter/lesson structure display in /phase-3/components/dashboard/CourseSidebar.tsx
- [ ] T023 [US1] Add progress indicators to navigation items in /phase-3/components/dashboard/CourseSidebar.tsx
- [ ] T024 [US1] Create responsive toggle functionality for sidebar in /phase-3/components/dashboard/CourseSidebar.tsx
- [ ] T025 [US1] Build main content window layout in /phase-3/components/dashboard/ContentWindow.tsx
- [ ] T026 [US1] Implement content rendering for different types in /phase-3/components/dashboard/ContentWindow.tsx
- [ ] T027 [US1] Create content navigation controls in /phase-3/components/dashboard/ContentControls.tsx
- [ ] T028 [US1] Add bookmarking functionality in /phase-3/components/dashboard/ContentControls.tsx
- [ ] T029 [US1] Implement responsive layout for sidebar/content in /phase-3/components/dashboard/DashboardLayout.tsx
- [ ] T030 [US1] Create mobile-friendly navigation in /phase-3/components/dashboard/MobileNav.tsx

## Phase 4: [US2] Progress Visuals

### Goal
Create React components for progress charts and streak visualizations.

### Independent Test Criteria
- Progress charts accurately display completion percentages
- Streak visualizations show consistent learning patterns
- Visual components are responsive and accessible
- Data updates properly reflect user progress

### Tasks
- [ ] T031 [US2] Create progress bar component in /phase-3/components/charts/ProgressBar.tsx
- [ ] T032 [US2] Implement circular progress chart in /phase-3/components/charts/CircularProgress.tsx
- [ ] T033 [US2] Build streak calendar visualization in /phase-3/components/charts/StreakCalendar.tsx
- [ ] T034 [US2] Create progress analytics dashboard in /phase-3/components/charts/ProgressAnalytics.tsx
- [ ] T035 [US2] Implement chart data formatting utilities in /phase-3/lib/chartUtils.ts
- [ ] T036 [US2] Add accessibility features to chart components in /phase-3/components/charts/
- [ ] T037 [US2] Create responsive chart layouts in /phase-3/components/charts/ResponsiveChartWrapper.tsx
- [ ] T038 [US2] Implement progress summary cards in /phase-3/components/dashboard/ProgressSummary.tsx
- [ ] T039 [US2] Add animation effects to progress components in /phase-3/components/charts/
- [ ] T040 [US2] Create progress export functionality in /phase-3/components/charts/ProgressExport.tsx

## Phase 5: [US3] Feature Integration

### Goal
Wire the 'Grounded Q&A' and 'Adaptive Path' features into the Web UI.

### Independent Test Criteria
- Grounded Q&A feature is accessible through the UI and connects to backend
- Adaptive Path feature provides personalized recommendations
- Premium access controls properly restrict advanced features
- Features integrate seamlessly with dashboard UI

### Tasks
- [ ] T041 [US3] Create grounded Q&A UI component in /phase-3/components/qa/GroundedQa.tsx
- [ ] T042 [US3] Implement Q&A input and response display in /phase-3/components/qa/GroundedQa.tsx
- [ ] T043 [US3] Connect Q&A component to backend API in /phase-3/services/qaService.ts
- [ ] T044 [US3] Add context awareness to Q&A component in /phase-3/components/qa/GroundedQa.tsx
- [ ] T045 [US3] Create adaptive learning path UI in /phase-3/components/learning/AdaptivePath.tsx
- [ ] T046 [US3] Implement path recommendation display in /phase-3/components/learning/AdaptivePath.tsx
- [ ] T047 [US3] Connect adaptive path to backend API in /phase-3/services/learningService.ts
- [ ] T048 [US3] Add user preference settings for path customization in /phase-3/components/learning/PathPreferences.tsx
- [ ] T049 [US3] Implement premium access checks for advanced features in /phase-3/components/learning/PremiumGate.tsx
- [ ] T050 [US3] Create fallback UI for non-premium users in /phase-3/components/learning/BasicPath.tsx

## Phase 6: [US4] Admin View

### Goal
Implement a basic admin dashboard for user analytics and cost tracking.

### Independent Test Criteria
- Admin dashboard displays user analytics effectively
- Cost tracking information is visible and accurate
- Access controls properly restrict admin features
- Dashboard provides actionable insights for administrators

### Tasks
- [ ] T051 [US4] Create admin dashboard layout in /phase-3/components/admin/AdminDashboard.tsx
- [ ] T052 [US4] Implement user analytics display in /phase-3/components/admin/UserAnalytics.tsx
- [ ] T053 [US4] Build cost tracking visualization in /phase-3/components/admin/CostTracking.tsx
- [ ] T054 [US4] Add subscription management UI in /phase-3/components/admin/SubscriptionManagement.tsx
- [ ] T055 [US4] Create admin authentication checks in /phase-3/components/admin/AdminProtectedRoute.tsx
- [ ] T056 [US4] Implement course management interface in /phase-3/components/admin/CourseManagement.tsx
- [ ] T057 [US4] Add user progress monitoring in /phase-3/components/admin/UserProgressMonitor.tsx
- [ ] T058 [US4] Create usage statistics display in /phase-3/components/admin/UsageStatistics.tsx
- [ ] T059 [US4] Implement feature usage analytics in /phase-3/components/admin/FeatureAnalytics.tsx
- [ ] T060 [US4] Add admin export functionality in /phase-3/components/admin/AdminExport.tsx

## Phase 7: [US5] Backend Consolidation

### Goal
Consolidate Phase 1 and Phase 2 routes into a single FastAPI backend interface.

### Independent Test Criteria
- All Phase 1 deterministic features are accessible through consolidated API
- All Phase 2 hybrid features are accessible through consolidated API
- Premium access controls are properly enforced at the API level
- API responses maintain consistent format across all endpoints

### Tasks
- [ ] T061 [US5] Create consolidated API router in /phase-3/backend/api/consolidated_router.py
- [ ] T062 [US5] Migrate Phase 1 content delivery routes to consolidated API in /phase-3/backend/api/content_routes.py
- [ ] T063 [US5] Migrate Phase 1 navigation routes to consolidated API in /phase-3/backend/api/navigation_routes.py
- [ ] T064 [US5] Migrate Phase 1 progress tracking routes to consolidated API in /phase-3/backend/api/progress_routes.py
- [ ] T065 [US5] Migrate Phase 2 adaptive learning routes to consolidated API in /phase-3/backend/api/adaptive_routes.py
- [ ] T066 [US5] Migrate Phase 2 assessment routes to consolidated API in /phase-3/backend/api/assessment_routes.py
- [ ] T067 [US5] Migrate Phase 2 synthesis routes to consolidated API in /phase-3/backend/api/synthesis_routes.py
- [ ] T068 [US5] Implement premium access middleware for hybrid features in /phase-3/backend/middleware/premium_check.py
- [ ] T069 [US5] Create unified response models in /phase-3/backend/schemas/
- [ ] T070 [US5] Add API documentation with OpenAPI in /phase-3/backend/main.py

## Phase 8: [US6] Quality Assurance

### Goal
Verify the web app is responsive and follows the 'Zero-Backend-LLM default' for non-premium features.

### Independent Test Criteria
- Web app is fully responsive across all device sizes
- Non-premium features operate without LLM calls
- Premium features are properly gated and isolated
- Performance meets specified requirements

### Tasks
- [ ] T071 [US6] Create responsive design tests in /phase-3/tests/responsive.test.ts
- [ ] T072 [US6] Implement mobile device compatibility checks in /phase-3/tests/mobile.test.ts
- [ ] T073 [US6] Test tablet layout responsiveness in /phase-3/tests/tablet.test.ts
- [ ] T074 [US6] Verify non-premium features have zero LLM calls in /phase-3/tests/compliance.test.ts
- [ ] T075 [US6] Test premium feature isolation in /phase-3/tests/premium_access.test.ts
- [ ] T076 [US6] Conduct performance testing for core features in /phase-3/tests/performance.test.ts
- [ ] T077 [US6] Verify access control implementation in /phase-3/tests/security.test.ts
- [ ] T078 [US6] Test API response consistency across endpoints in /phase-3/tests/api_consistency.test.ts
- [ ] T079 [US6] Validate accessibility compliance in /phase-3/tests/accessibility.test.ts
- [ ] T080 [US6] Complete end-to-end integration testing in /phase-3/tests/e2e.test.ts

## Dependencies

### User Story Completion Order
1. Setup (T001-T010) → Foundational (T011-T020) → US1 Dashboard UI → US2 Progress Visuals → US3 Feature Integration → US4 Admin View → US5 Backend Consolidation → US6 Quality Assurance

### Blocking Dependencies
- T001-T010 (Setup) must be completed before other phases
- T011-T020 (Foundational) required for all user stories
- T061-T070 (Backend Consolidation) required for frontend feature integration
- T021-T030 (Dashboard UI) needed before feature integration
- T031-T040 (Progress Visuals) needed for feature integration

## Parallel Execution Examples

### Per User Story
- US1: T021, T022, T023 (sidebar components) can run in parallel with T025, T026 (content window components)
- US2: T031, T032, T033 (chart components) can run in parallel with T036, T037 (accessibility and layout)
- US3: T041, T042 (Q&A UI) can run in parallel with T045, T046 (Adaptive Path UI)
- US4: T051, T052 (admin layout and analytics) can run in parallel with T054, T056 (management interfaces)
- US5: T062, T063, T064 (Phase 1 routes) can run in parallel with T065, T066, T067 (Phase 2 routes)

## Implementation Strategy

### MVP First Approach
1. Start with basic Next.js setup and layout (T001-T010)
2. Add foundational components (T011-T020)
3. Implement core dashboard UI (T021-T030)
4. Add basic progress visualization (T031-T040)
5. Integrate core features (T041-T050)
6. Add admin functionality (T051-T060)
7. Consolidate backend (T061-T070)
8. Complete QA (T071-T080)

### Incremental Delivery
- Sprint 1: Setup and foundational components (T001-T020)
- Sprint 2: Dashboard UI and progress visuals (T021-T040)
- Sprint 3: Feature integration (T041-T050)
- Sprint 4: Admin view and backend consolidation (T051-T070)
- Sprint 5: Quality assurance and final testing (T071-T080)