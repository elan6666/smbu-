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

## V2 Read-Only Reviews

- Context/router QA: `019f1992-aa6c-7fe3-a96b-4447012bd2f3`
  - Scope: multi-turn context behavior, current-message history compatibility, program follow-up routing.
  - Result: fail before fixes.
  - Handoff file: `.byte-os/subagents/context-route-review-019f1992-aa6c.md`
- Report/delivery QA: `019f1992-e66b-7833-b82f-bbd2fb2536d3`
  - Scope: report claims, training artifact support, Qwen metadata correctness.
  - Result: fail before fixes.
  - Handoff file: `.byte-os/subagents/report-delivery-review-019f1992-e66b.md`

## V2 Main-Agent Merge Status

- History that includes the current user message no longer breaks “刚才我问了什么”; the resolver skips the current message.
- Exact program questions such as `人工智能怎么样` no longer include broad keyword pollution from unrelated program rows.
- Report no longer claims 7B training before artifacts exist; it now uses the completed server training metrics.
- Training script metadata now records the actual model name and QLoRA vs LoRA method.
- Server Qwen is now Qwen2.5-7B-Instruct with `models/qwen7b_lora`, not the earlier 0.5B runtime.
