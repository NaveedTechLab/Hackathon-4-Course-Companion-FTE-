<!--
Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: Core Mission, Project Structure, Architectural Rules, Workflow Constraints, Exit Criteria
Removed sections: None
Templates requiring updates: N/A
Follow-up TODOs: None
-->
# Course Companion FTE Project Constitution

## Core Principles

### I. Digital FTE Mission
Build a Digital FTE educational tutor working 168 hours/week. The system must provide continuous, reliable educational support equivalent to a full-time human tutor, available 24/7 to assist students with their learning needs.
Rationale: To create an always-available educational companion that provides consistent, high-quality support to students regardless of time or location.

### II. Zero-Backend-LLM Principle
Adhere to the Zero-Backend-LLM principle: Backend performs zero LLM inference in Phase 1. The backend must remain completely deterministic with no direct calls to LLM APIs, RAG systems, or AI agent loops.
Rationale: To ensure reliability, predictability, and cost control in the foundational phase of the system while maintaining data privacy and system stability.

### III. Phased Development Approach
Implement sequential phase development: Phase 1 (ChatGPT App + Deterministic FastAPI + R2 Content), Phase 2 (Hybrid Intelligence + Claude Agent SDK + Premium Gating), Phase 3 (Next.js Web App + Consolidated Backend). Each phase must be completed before advancing to the next.
Rationale: To ensure manageable complexity, proper testing, and validation of core functionality before introducing advanced features.

### IV. Strict Architectural Boundaries
Phase 1 Backend: Strictly deterministic. Forbidden: LLM API calls, RAG summarization, or agent loops. Phase 2: Hybrid features must be selective, premium-gated, and user-initiated. Data Layer: Cloudflare R2 for content; Neon/Supabase for progress tracking.
Rationale: To maintain architectural integrity and ensure compliance with Zero-Backend-LLM principle while enabling controlled introduction of AI features in later phases.

### V. Sequential Execution Workflow
Follow sequential execution: Spec → Plan → Tasks → Implement. No skipping steps. Specs are treated as binding contracts that must be fulfilled before moving forward.
Rationale: To ensure proper planning, comprehensive coverage of requirements, and systematic development that reduces risk of missed requirements or architectural flaws.

### VI. Evidence-Based Feature Addition
Phase 2 hybrid features must have clear cost/value justification. Maximum of 2 hybrid features allowed initially. All features must demonstrate measurable educational value before implementation.
Rationale: To prevent feature creep and ensure that AI enhancements provide genuine educational value rather than unnecessary complexity.

## Project Structure

### Phase Organization
- `/phase-1` (ChatGPT App + Deterministic FastAPI + R2 Content)
- `/phase-2` (Hybrid Intelligence + Claude Agent SDK + Premium Gating)
- `/phase-3` (Next.js Web App + Consolidated Backend)
- `/skills` (SKILL.md files for runtime agent behavior)
- `/docs` (Architecture, Cost Analysis, and API Specs)

### Technology Stack Requirements
- Phase 1: FastAPI backend with deterministic logic only, Cloudflare R2 for content storage, Neon or Supabase for progress tracking
- Phase 2: Claude Agent SDK for selective AI features with premium gating
- Phase 3: Next.js for responsive web application

## Development Workflow

### Sequential Execution Requirements
- All work must follow Spec → Plan → Tasks → Implement sequence
- No phase skipping allowed
- Each phase must meet exit criteria before advancement
- Specs are binding contracts requiring formal amendment process for changes

### Quality Gates
- Phase 1: Zero LLM calls verified by code audit, 6 core features functional
- Phase 2: Maximum 2 hybrid features implemented, clear cost/value justification documented
- Phase 3: Fully responsive standalone Web App meeting all requirements

### Code Review Requirements
- All code must undergo Zero-Backend-LLM compliance verification in Phase 1
- LLM integration detection using automated tools
- Deterministic behavior validation
- Performance and security compliance checks

## Governance

All development activities must comply with this constitution. Any deviation requires formal amendment process with clear justification. The constitution supersedes all other development practices and guidelines. Code audits must verify compliance with Zero-Backend-LLM principle. All pull requests must include evidence of constitutional compliance.

**Version**: 1.0.0 | **Ratified**: 2026-01-27 | **Last Amended**: 2026-01-27