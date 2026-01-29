---
id: 6
title: course-companion-constitution-update
stage: constitution
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: sp.constitution
labels: ["constitution", "governance", "project-structure", "zero-backend-llm"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml:
  - constitution validation completed
  - version incremented to 1.0.0
  - all principles properly implemented
prompt_text: |
  Establish the Course Companion FTE Project Constitution:

  1. CORE MISSION:
     - Build a Digital FTE educational tutor working 168 hours/week.
     - Adhere to the Zero-Backend-LLM principle: Backend performs zero LLM inference in Phase 1.

  2. PROJECT STRUCTURE:
     - /phase-1 (ChatGPT App + Deterministic FastAPI + R2 Content).
     - /phase-2 (Hybrid Intelligence + Claude Agent SDK + Premium Gating).
     - /phase-3 (Next.js Web App + Consolidated Backend).
     - /skills (SKILL.md files for runtime agent behavior).
     - /docs (Architecture, Cost Analysis, and API Specs).

  3. STRICT ARCHITECTURAL RULES:
     - Phase 1 Backend: Strictly deterministic. Forbidden: LLM API calls, RAG summarization, or agent loops.
     - Phase 2: Hybrid features must be selective, premium-gated, and user-initiated.
     - Data Layer: Cloudflare R2 for content; Neon/Supabase for progress tracking.

  4. WORKFLOW CONSTRAINTS:
     - Sequential execution: Spec -> Plan -> Tasks -> Implement.
     - One phase at a time; no skipping steps.
     - Specs are treated as binding contracts.

  5. EXIT CRITERIA:
     - Phase 1: Zero LLM calls in code audit; 6 core features functional.
     - Phase 2: Max 2 hybrid features; clear cost/value justification.
     - Phase 3: Fully responsive standalone Web App.
response_text: |
  Successfully updated the Course Companion FTE Project Constitution with:
  - Six core principles including Digital FTE Mission and Zero-Backend-LLM compliance
  - Clear project structure for all three phases
  - Sequential execution workflow requirements
  - Quality gates and exit criteria for each phase
  - Code review requirements for LLM compliance
  - Version 1.0.0 with proper ratification date
outcome: |
  Course Companion FTE Project Constitution successfully established with comprehensive
  governance framework for Zero-Backend-LLM compliance and phased development.
evaluation: |
  The constitution includes all required components and establishes clear governance
  for the project's architectural principles and development workflow.
---