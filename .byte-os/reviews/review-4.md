# Review 4: V2 Final Readiness

Date: 2026-07-01

## Review Inputs

- Context/router subagent: `019f1992-aa6c-7fe3-a96b-4447012bd2f3`
- Report/delivery subagent: `019f1992-e66b-7833-b82f-bbd2fb2536d3`
- Local tests, remote tests, server Qwen health, training artifacts, and compiled PDF.

## Initial Verdict

Fail before V2 fixes.

## Findings And Status

- Context recall could fail when frontend history included the current message.
  - Status: fixed and tested.
- Exact program questions could include unrelated broad program rows.
  - Status: fixed and tested.
- Report overclaimed completed 7B training before artifacts existed.
  - Status: fixed after server training completed.
- Qwen training metadata was too hardcoded.
  - Status: fixed.

## Verification

- Local `pytest`: 29 passed.
- Local focused tests: 22 passed.
- Local compileall: passed.
- Server focused tests: 22 passed.
- Server compileall: passed.
- Server `/api/qwen-health`: Qwen2.5-7B-Instruct, CUDA, adapter `models/qwen7b_lora`.
- Qwen2.5-7B QLoRA training: train loss 0.021, eval loss 0.022.
- LaTeX PDF: compiled and copied to `report/smbu-admission-dialogue-report.pdf`.

## Residual Risks

- Score data coverage is still strongest for the current Guangdong examples.
- Retrieval remains lexical; dense embedding and reranking would improve semantic recall.
- Qwen is intentionally bypassed for structured facts, so fluent generation is limited on score/certificate/count answers by design.

## Verdict

Ship.
