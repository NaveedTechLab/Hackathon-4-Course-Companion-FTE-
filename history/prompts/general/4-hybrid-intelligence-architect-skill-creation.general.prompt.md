---
id: 4
title: hybrid-intelligence-architect-skill-creation
stage: general
date_iso: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: skill-creator
labels: ["skill", "llm", "claude", "hybrid", "intelligence", "education"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/hybrid-intelligence-architect/SKILL.md
  - .claude/skills/hybrid-intelligence-architect/README.md
  - .claude/skills/hybrid-intelligence-architect/references/llm-integration-patterns.md
  - .claude/skills/hybrid-intelligence-architect/references/premium-features.md
  - .claude/skills/hybrid-intelligence-architect/references/deterministic-logic-isolation.md
  - .claude/skills/hybrid-intelligence-architect/scripts/generate-feature-guard.py
  - .claude/skills/hybrid-intelligence-architect/scripts/generate-claude-integration.py
  - .claude/skills/hybrid-intelligence-architect/assets/implementation-patterns.md
tests_yaml:
  - skill validation completed
  - script executables verified
  - reference documentation created
prompt_text: |
  Create a skill named "hybrid-intelligence-architect" with description "Expert in selective LLM integration using Claude Agent SDK. Specialized in implementing premium-gated features like adaptive learning paths and LLM-graded assessments while maintaining strict isolation from deterministic logic."
response_text: |
  Created the Hybrid Intelligence Architect skill with:
  - Core SKILL.md with YAML frontmatter and hybrid intelligence guidelines
  - Reference documentation for LLM integration, premium features, and deterministic logic isolation
  - Scripts for generating feature guards and Claude integration patterns
  - Asset templates for implementation patterns
  - Proper directory structure with scripts, references, and assets
outcome: |
  Successfully created the hybrid-intelligence-architect skill with comprehensive documentation
  and tools for building hybrid intelligence systems with Claude Agent SDK.
evaluation: |
  The skill includes all required components and follows best practices for
  hybrid intelligence system design with proper isolation between AI and deterministic logic.
---