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
  - Status: helper service and backend hook exist; server runtime must report `qwen_configured=true` before claiming Qwen is enabled.
- Server deployment was still on old code during the subagent review.
  - Status: pending current commit, push, server pull, restart, and remote smoke.

## Current Local Verdict

Ship locally after iteration 4.

## Required Before Final Handoff

- Commit and push v1 changes.
- Pull and restart server deployment.
- Attempt to start local Qwen service on the server.
- Verify server `/api/health`, greeting, clarification, undergraduate program, undergraduate enrollment boundary, and graduate enrollment answers.
