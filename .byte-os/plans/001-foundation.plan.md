---
id: 001
title: Foundation Setup
status: complete
wave: 1
owner_role: Tech Lead
depends_on: []
start_directory: .
context_files: [.byte-os/BYTE.md, .byte-os/TECH_SPEC.md, .byte-os/DECISIONS.md]
agents_context_stack: []
subagent_policy: none
---

# Goal

Create a reproducible repository foundation for the SMBU admissions dialogue system.

# OKR Link

KR5, KR6

# Scope

Repository remote, project layout, dependency files, run scripts, README, and basic health checks.

# Non-Goals

No final model quality claims. No server deployment in this plan.

# Steps

## Step 1: Configure repository foundation

- Purpose: Make the project source-controlled and runnable from a clean checkout.
- Actions:
  - Add GitHub remote if missing.
  - Create backend, scripts, data, frontend, tests, and report directories.
  - Add dependency and environment documentation.
- Files or modules:
  - `README.md`
  - `requirements.txt`
  - `.gitignore`
  - project directories
- Expected output: A clear project shell.
- Step verification: `git remote -v`, `find . -maxdepth 2 -type f`.
- Subagent: none

## Step 2: Add minimal application entry points

- Purpose: Establish commands that later plans can extend.
- Actions:
  - Add FastAPI app shell.
  - Add static frontend shell.
  - Add CLI scripts for ingest, train, evaluate.
- Files or modules:
  - `app/`
  - `scripts/`
  - `frontend/`
- Expected output: Importable backend and callable scripts.
- Step verification: `python -m compileall app scripts`.
- Subagent: none

# Dependencies

None.

# Scoped Commands

- Test: `pytest`
- Lint: not configured in v0
- Typecheck: not configured in v0
- Build: `python -m compileall app scripts`

# AGENTS.md Context

- Root context: none yet.
- Module context: none.
- Scoped command source: this plan.
- Safe edit boundaries: repository root except `.git`.
- Missing or stale AGENTS.md notes: no project-level AGENTS.md exists yet.

# Subagent Plan

- Exploration subagents: none.
- Implementation subagents: none.
- Review subagents: after core workflow exists.
- Isolation boundaries: not applicable.
- Merge or handoff notes: main agent owns initial foundation.

# Code Change Guardrails

Keep the foundation small and avoid unused frameworks.

# Acceptance Criteria

- Repository has a documented layout.
- Backend app imports.
- Scripts compile.
- Remote origin is configured or the reason is recorded.

# Verification

- `python -m compileall app scripts`
- `git status --short --branch`

# Experiment Or Measurement

Not applicable.

# Risks

Remote push may require credentials; local work can continue before push.

# Notes

This plan is the first build wave.
