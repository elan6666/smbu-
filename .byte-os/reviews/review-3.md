# Review 3: Subagent-Guided V1 Readiness Review

Date: 2026-06-30

## Review Inputs

- Product/data QA subagent: `019f182e-9a00-7f90-a098-2d25db5dc8c8`
- Code QA subagent: `019f182e-7d7c-7ad2-8d59-e49f48cdac19`

## Initial Verdict

Fail before iteration 4.

## Findings And Status

- Greeting and vague follow-up questions dumped unrelated retrieval results.
  - Status: fixed with `greeting` and `clarification` routes.
- Exact program query could be broadened by degree-mode matching.
  - Status: fixed by keeping exact program filtering when asking single/double comparison.
- Undergraduate enrollment counts were not fully available from official structured pages.
  - Status: fixed by recording directly available rows and explicit source boundaries instead of inventing counts.
- Graduate program rows used stale enrollment counts.
  - Status: fixed using the 2026 master admission page's 18 official directions and plan numbers.
- Evaluation did not check structured program/dimension rows.
  - Status: fixed in `scripts/evaluate_system.py` and tests.
- Qwen was only an optional hook.
  - Status: fixed. The server runs a local Qwen/OpenAI-compatible service and `/api/health` reports `qwen_configured=true`.
- Server deployment was still on old code during the subagent review.
  - Status: fixed. Server tests and remote smoke passed after v1 redeploy.

## Current Local Verdict

Ship.

## Required Before Final Handoff

- No blocking item remains.
