---
id: 004
title: Web Demo And API
status: complete
wave: 3
owner_role: Full Stack Engineer
depends_on: [002, 003]
start_directory: .
context_files: [.byte-os/UX_SPEC.md, .byte-os/TECH_SPEC.md]
agents_context_stack: []
subagent_policy: none
---

# Goal

Deliver a usable Web chat demo backed by the retrieval, score, and routing layers.

# OKR Link

KR2, KR5

# Scope

FastAPI endpoints, static frontend, chat flow, source display, score table display, and error states.

# Non-Goals

No production authentication. No complex admin dashboard.

# Steps

## Step 1: Implement API endpoints

- Purpose: Expose backend capabilities.
- Actions:
  - Implement `/api/health`, `/api/search`, `/api/scores`, `/api/chat`, `/api/sources`.
- Files or modules:
  - `app/main.py`
  - `app/schemas.py`
- Expected output: API returns JSON for core workflows.
- Step verification: FastAPI test client tests.
- Subagent: none

## Step 2: Implement static chat UI

- Purpose: Provide course demo surface.
- Actions:
  - Build single-page HTML/CSS/JS UI served by FastAPI.
  - Show answer, sources, and score rows.
- Files or modules:
  - `frontend/`
  - `app/main.py`
- Expected output: User can chat in browser.
- Step verification: open local URL and run API smoke calls.
- Subagent: none

## Step 3: Add grounded answer generation fallback

- Purpose: Ensure demo works before heavy model deployment.
- Actions:
  - Compose answer from retrieved snippets and structured rows.
  - Keep optional Qwen/local model hook configurable.
- Files or modules:
  - `app/generator.py`
- Expected output: Robust local fallback with source citations.
- Step verification: representative chat requests.
- Subagent: none

# Dependencies

Plans 002 and 003.

# Scoped Commands

- Test: `pytest tests/test_api.py`
- Lint: not configured
- Typecheck: not configured
- Build: `python -m compileall app`

# AGENTS.md Context

- Root context: none.
- Module context: none.
- Scoped command source: this plan.
- Safe edit boundaries: `app/`, `frontend/`, `tests/`.
- Missing or stale AGENTS.md notes: none.

# Subagent Plan

None.

# Code Change Guardrails

Keep UI focused on chat, profile, sources, and score evidence.

# Acceptance Criteria

- Web demo loads.
- Chat endpoint answers representative questions.
- Evidence appears in the response.
- Score questions return structured rows or clear missing-data text.

# Verification

- `pytest tests/test_api.py`
- Manual browser smoke test.

# Experiment Or Measurement

Record demo screenshots and representative API responses for the report.

# Risks

Frontend polish can consume time; prioritize clarity and evidence display.

# Notes

FastAPI static serving is acceptable for v0.
