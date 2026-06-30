---
id: 007
title: Context Memory And Qwen2.5-7B QLoRA Fine-Tuning
status: complete
wave: 7
owner_role: Full Stack / ML Engineer
depends_on: [003, 004, 005, 006]
start_directory: .
context_files: [.byte-os/TECH_SPEC.md, .byte-os/UX_SPEC.md, .byte-os/STATUS.md]
agents_context_stack: [AGENTS.md]
subagent_policy: review_only
---

# Goal

Upgrade the delivered SMBU admissions assistant with short multi-turn context support, Qwen2.5-7B QLoRA fine-tuning evidence, report updates, placeholder demo screenshots, and server deployment.

# OKR Link

KR4, KR5, KR6

# Scope

- Add request/response schema support for recent chat history.
- Add context-aware behavior for "上面说了什么", "刚才我问了什么", "这个/它/继续" follow-ups.
- Improve routing for assistant identity and major follow-up questions.
- Generate Qwen SFT examples for evidence-grounded admissions dialogue and multi-turn follow-up.
- Add Qwen2.5-7B QLoRA training and evaluation scripts.
- Run server-side training on the 2 x RTX 5090 host and capture loss/evaluation artifacts.
- Update the LaTeX report and PDF to describe 7B QLoRA and context support.
- Replace current demo figure slots with placeholders for new V2 screenshots.

# Non-Goals

- No full-parameter fine-tuning.
- Do not store admissions facts only in model weights.
- Do not remove deterministic structured table answering for score/certificate/enrollment facts.
- Do not add user accounts, persistent private history, or long-term memory.

# Acceptance Criteria

- `/api/chat` accepts `history` and handles at least:
  - "刚才我问了什么"
  - "上面说了什么"
  - "这个专业怎么样"
  - "它是双学籍吗"
  - "你是什么助手"
- Frontend sends recent chat history.
- Tests cover context follow-up and identity/major routing failures from the user screenshot.
- Qwen2.5-7B QLoRA script exists and produces training/eval loss artifacts on the server.
- Fine-tuning evaluation includes before/after examples or metric summary.
- Report includes 7B QLoRA method, training setup, loss figure/table, context ability, and V2 screenshot placeholders.
- Server demo is restarted and health checks pass.

# Verification

- `pytest`
- `python -m compileall app scripts`
- `python scripts/train_intent.py`
- `python scripts/evaluate_system.py`
- `python scripts/build_sft_dataset.py`
- server QLoRA smoke/full run
- server `/api/health`, `/api/qwen-health`, and context API smoke
- `tectonic -X compile report/main.tex --outdir report/build`

# Risks

- Qwen2.5-7B download or training may fail due to network, Hugging Face access, CUDA/torch compatibility, or disk constraints.
- If 7B training is blocked, keep the scripts and dataset complete, record the blocker, and fall back to a smaller model only with explicit evidence.
- Context rewriting must not cause structured factual answers to lose table guardrails.

# Completion Evidence

- Local context/routing tests passed: `pytest tests/test_api.py tests/test_router.py` -> 22 passed.
- Local full test suite passed after V2 changes: `pytest` -> 29 passed.
- SFT data built: 960 examples, 840 train, 120 eval.
- Server Qwen2.5-7B QLoRA training completed: 2 epochs, 210 steps, final train loss 0.021, final eval loss 0.022.
- Server Qwen health passed with `Qwen/Qwen2.5-7B-Instruct` and adapter `models/qwen7b_lora`.
- Server focused tests passed: 22 passed.
- Report PDF regenerated with Qwen 7B method, training curve, context flow, data-source table, and V2 screenshot placeholders.
