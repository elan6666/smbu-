# Subagents

Subagent mode: on for v1 review.

## Completed Read-Only Reviews

- Product/data QA: `019f182e-9a00-7f90-a098-2d25db5dc8c8`
  - Scope: applicant-facing completeness, official data boundaries, deployment readiness.
  - Result: fail before iteration 4.
  - Handoff file: `.byte-os/subagents/product-data-qa-019f182e-9a00.md`
- Code QA: `019f182e-7d7c-7ad2-8d59-e49f48cdac19`
  - Scope: API correctness, routing, structured query behavior, tests.
  - Result: fail before iteration 4.
  - Handoff file: `.byte-os/subagents/code-qa-019f182e-7d7c.md`

## Main-Agent Merge Status

- Greeting and clarification route bug: fixed.
- Exact program filtering bug: fixed.
- Undergraduate enrollment boundary: fixed.
- 2026 master program/count/language data: fixed.
- Evaluation structured row checks: fixed.
- Qwen hook: implemented and server runtime verified with `qwen_configured=true`.
- Server deployment: verified on port 18080.
