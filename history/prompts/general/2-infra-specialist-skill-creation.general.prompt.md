---
id: 2
title: infra-specialist-skill-creation
stage: general
date_iso: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: skill-creator
labels: ["skill", "infrastructure", "cloudflare", "flyio", "railway", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .claude/skills/infra-specialist/SKILL.md
  - .claude/skills/infra-specialist/README.md
  - .claude/skills/infra-specialist/references/r2-storage.md
  - .claude/skills/infra-specialist/references/flyio-deployment.md
  - .claude/skills/infra-specialist/references/railway-deployment.md
  - .claude/skills/infra-specialist/references/database-integrations.md
  - .claude/skills/infra-specialist/scripts/deploy_to_fly.py
  - .claude/skills/infra-specialist/scripts/deploy_to_railway.py
  - .claude/skills/infra-specialist/scripts/r2_manager.py
  - .claude/skills/infra-specialist/assets/infrastructure-template.md
tests_yaml:
  - skill validation completed
  - script executables verified
  - reference documentation created
prompt_text: |
  Create a skill named "infra-specialist" with description "Specialist in configuring Cloudflare R2 for verbatim content storage and media assets. Experienced in deploying Python applications to Fly.io or Railway and managing Neon/Supabase database integrations for progress tracking."
response_text: |
  Created the Infra Specialist skill with:
  - Core SKILL.md with YAML frontmatter and infrastructure guidelines
  - Reference documentation for R2 storage, Fly.io, Railway, and database integrations
  - Scripts for deploying to Fly.io and Railway, plus R2 management
  - Asset templates for infrastructure configuration
  - Proper directory structure with scripts, references, and assets
outcome: |
  Successfully created the infra-specialist skill with comprehensive documentation
  and tools for managing cloud infrastructure with R2, Fly.io/Railway, and databases.
evaluation: |
  The skill includes all required components and follows best practices for
  infrastructure configuration and deployment automation.
---