---
id: 5
title: qa-auditor-skill-creation
stage: general
date_iso: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: skill-creator
labels: ["skill", "qa", "auditing", "compliance", "llm", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/qa-auditor/SKILL.md
  - .claude/skills/qa-auditor/README.md
  - .claude/skills/qa-auditor/references/auditing-techniques.md
  - .claude/skills/qa-auditor/references/remediation-strategies.md
  - .claude/skills/qa-auditor/scripts/audit_backend.py
  - .claude/skills/qa-auditor/scripts/remediate_violations.py
  - .claude/skills/qa-auditor/assets/remediation-templates.md
tests_yaml:
  - skill validation completed
  - script executables verified
  - reference documentation created
prompt_text: |
  Create a skill named "qa-auditor" with description "Specialized in code review and API auditing to ensure Zero-Backend-LLM compliance in Phase 1. Responsible for verifying that no forbidden LLM API calls, RAG summarization, or agent loops exist in the backend."
response_text: |
  Created the QA Auditor skill with:
  - Core SKILL.md with YAML frontmatter and Zero-Backend-LLM compliance guidelines
  - Reference documentation for auditing techniques and remediation strategies
  - Scripts for auditing and remediating LLM integration violations
  - Asset templates for remediation patterns
  - Proper directory structure with scripts, references, and assets
outcome: |
  Successfully created the qa-auditor skill with comprehensive documentation
  and tools for ensuring Zero-Backend-LLM compliance in codebases.
evaluation: |
  The skill includes all required components and follows best practices for
  code auditing and compliance verification.
---