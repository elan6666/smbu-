# Build Log

Date: 2026-06-30

## Mode

byte-auto

## Plans Executed

- 001 Foundation Setup: complete
- 002 Data Ingestion And RAG Core: complete
- 003 Lightweight Intent Training: complete
- 004 Web Demo And API: complete
- 005 Evaluation And LaTeX Report: complete
- 006 Server Deployment And Delivery: complete
- Iteration 4 V1 Admissions Data Expansion And Dialogue Logic Repair: local complete

## Files Changed

- Repository foundation: `README.md`, `.gitignore`, `requirements.txt`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`
- Backend: `app/`, including program/dimension query endpoints and optional Qwen hook
- Scripts: `scripts/`
- Data: `data/sources.json`, `data/structured/admission_scores.csv`, `data/structured/programs.csv`, `data/structured/admission_dimensions.csv`, `data/training/intent_examples.csv`, `data/eval/questions.csv`, `data/eval/prospective_questions.csv`
- Frontend: `frontend/`
- Tests: `tests/`
- Report: `report/main.tex`, `report/references.bib`, `report/*.tex`, `report/smbu-admission-dialogue-report.pdf`
- Byte OS: `.byte-os/`
- Optional Qwen helper: `requirements-qwen.txt`, `scripts/serve_qwen_openai.py`

## V1 Verification Run

- Ingest: `python scripts/ingest_sources.py --limit 20`
  - documents: 13
  - fetched: 10
  - fallback: 3
- Training: `python scripts/train_intent.py`
  - accuracy: 0.9375
  - macro-F1: 0.8974
- Evaluation: `python scripts/evaluate_system.py`
  - questions: 58
  - router accuracy: 0.7586
  - source coverage: 1.000
  - average answer length: 1546.6
- Tests: `pytest`
  - 18 passed
- Compile: `python -m compileall app scripts`
  - passed
- LaTeX: compile `report/main.tex`
  - PDF generated at `report/build/main.pdf`
  - copied to `report/smbu-admission-dialogue-report.pdf`
- Local API smoke:
  - `你好`: greeting, no sources
  - `啥意思`: clarification, no sources
  - `电子与计算机工程是单学籍还是双学籍？`: one undergraduate program row, single学籍
  - `本科招生人数是多少？`: official boundary plus directly available 10-person foreign-language recommended row
  - `纳米生物技术硕士是英语教学吗，招多少人？`: English teaching, 15 students
  - `硕士有哪些专业和招生人数？`: 18 official 2026 master directions
- Server Qwen smoke:
  - Qwen helper service ran on `127.0.0.1:18082` with `Qwen/Qwen2.5-0.5B-Instruct` and CUDA.
  - Initial smoke showed Qwen could rewrite structured numbers incorrectly.
  - Backend policy was tightened so Qwen is skipped for structured招生事实 and only used for non-structured evidence wording.
  - Final server smoke passed with `qwen_configured=true`, correct greeting/clarification behavior, and correct structured answers for本科/硕士招生 facts.

## Verification Run

- Dependency install: `pip install -r requirements.txt`
- Ingest: `python scripts/ingest_sources.py --limit 8`
  - documents: 7
  - fetched: 5
  - fallback: 2
- Training: `python scripts/train_intent.py`
  - accuracy: 0.900
  - macro-F1: 0.852
- Evaluation: `python scripts/evaluate_system.py`
  - questions: 50
  - router accuracy: 0.760
  - source coverage: 1.000
- Tests: `pytest`
  - 8 passed
- Compile: `python -m compileall app scripts`
  - passed
- LaTeX: compile `report/main.tex`
  - PDF generated at `report/build/main.pdf`
  - copied to `report/smbu-admission-dialogue-report.pdf`
- Local Web smoke:
  - `/api/health` returned `ok`
  - `/api/chat` returned real 2025/2024 Guangdong score rows and evidence sources
  - `/` returned HTTP 200
- GitHub:
  - `git push -u origin main` succeeded
- Server:
  - clone path: `/data/yilangliu/smbu-admission-assistant`
  - dependency install: passed using user-level `virtualenv`
  - ingestion: 7 documents, 4 fetched, 3 fallback
  - training: accuracy 0.900, macro-F1 0.852
  - evaluation: 50 questions, router accuracy 0.760, source coverage 1.000
  - pytest: 8 passed
  - compileall: passed
  - FastAPI: running on `0.0.0.0:18080`
  - local health check to `http://10.24.1.91:18080/api/health`: passed

## Code Rule Notes

- RAG-first architecture preserved.
- Light training is used for routing, not factual memory.
- Structured score data includes source notes and uncertainty boundaries.
- UI is intentionally simple: chat, profile, source panel, score rows.

## Subagents Used

- Product/data QA subagent `019f182e-9a00-7f90-a098-2d25db5dc8c8`: failed v1 readiness before fixes; findings recorded in `.byte-os/subagents/product-data-qa-019f182e-9a00.md`.
- Code QA subagent `019f182e-7d7c-7ad2-8d59-e49f48cdac19`: failed v1 readiness before fixes; findings recorded in `.byte-os/subagents/code-qa-019f182e-7d7c.md`.

## AGENTS.md Context Stack Used

- `AGENTS.md`
- `.byte-os/CODEBASE_MAP.md`
- `.byte-os/HARNESS.md`
- `.byte-os/AGENTS_AUDIT.md`

## Failures Or Blockers

- Port 8000 was occupied locally; local smoke used port 8001.
- Some official pages returned HTTP errors; fallback source records were preserved.
- Score rows use third-party score summary plus government news context where official school-structured rows were not directly available.

## OKR Impact

- KR1: source ingestion completed.
- KR2: structured score lookup completed for Guangdong sample rows.
- KR3: 50-question evaluation completed.
- KR4: lightweight router training completed.
- KR5: local Web demo and server deployment completed.
- KR6: LaTeX PDF compiled.

## Next Wave

No required wave remains for v1. Optional: broader province data, dense embeddings/reranker, and demo video.

## V2 Build Log

Date: 2026-07-01

### Plans Executed

- 007 Context Memory And Qwen2.5-7B QLoRA Fine-Tuning: in progress

### Files Changed

- Backend: `app/context.py`, `app/main.py`, `app/router.py`, `app/llm.py`, `app/schemas.py`
- Frontend: `frontend/app.js`
- Training: `scripts/build_sft_dataset.py`, `scripts/finetune_qwen_lora.py`, `scripts/evaluate_finetuned_qwen.py`, `requirements-qwen.txt`
- Serving: `scripts/serve_qwen_openai.py`
- Tests: `tests/test_api.py`
- Data: `data/finetune/sft_examples.jsonl`, `data/finetune/sft_summary.json`, `data/training/intent_examples.csv`, `data/eval/questions.csv`
- Report: `report/main.tex`, `report/references.bib`, `report/qwen_finetune_metrics.tex`, `report/smbu-admission-dialogue-report.pdf`

### Local Verification

- SFT data: `python scripts/build_sft_dataset.py --target-size 960`
  - count: 960
  - train: 840
  - eval: 120
  - kinds: assistant identity, context pronoun, program grounding, score guardrail, future-score refusal
- Tests: `pytest`
  - 28 passed before subagent fixes
- Focused tests after subagent fixes: `pytest tests/test_api.py tests/test_router.py`
  - 22 passed
- Compile: `python -m compileall app scripts`
  - passed
- Intent training: `python scripts/train_intent.py`
  - accuracy: 0.950
  - macro-F1: 0.905
- System evaluation: `python scripts/evaluate_system.py`
  - questions: 63
  - router accuracy: 0.794
  - source coverage: 1.000
- LaTeX: `tectonic -X compile report/main.tex --outdir report/build`
  - passed
  - copied to `report/smbu-admission-dialogue-report.pdf`

### Subagent Review Findings And Fixes

- Fixed API compatibility where history might include the current user message; context recall now skips the current question.
- Fixed program-row pollution for exact program questions such as `人工智能怎么样` and pronoun follow-up `它是双学籍吗`.
- Fixed report wording that implied server Qwen2.5-7B training was complete before loss artifacts existed.
- Fixed training script metadata so model/method reflect actual `--model` and QLoRA vs bf16 LoRA fallback.

### Server Progress

- Server path: `/data/yilangliu/smbu-admission-assistant`
- GPU: two NVIDIA GeForce RTX 5090 GPUs available.
- Dependencies: `peft`, `bitsandbytes`, `datasets`, and `matplotlib` installed.
- Direct Hugging Face access timed out; `HF_ENDPOINT=https://hf-mirror.com` works.
- Qwen2.5-7B smoke training succeeded.
- Qwen2.5-7B full QLoRA training succeeded: 2 epochs, 210 steps, final train loss 0.021, final eval loss 0.022.
- Adapter saved on server at `models/qwen7b_lora`.
- Training artifacts copied back locally:
  - `report/qwen_finetune_metrics.tex`
  - `report/figures/qwen7b-lora-loss.png`
  - `artifacts/finetune/qwen7b_lora_metrics.json`
  - `artifacts/finetune/qwen7b_lora_log_history.json`
- Qwen helper service restarted on `127.0.0.1:18082` with `Qwen/Qwen2.5-7B-Instruct` and adapter `models/qwen7b_lora`.
- Web backend restarted on `0.0.0.0:18080` with `QWEN_API_URL=http://127.0.0.1:18082/v1/chat/completions`.
- Remote health:
  - `/api/health`: `qwen_configured=true`
  - `/api/qwen-health`: model `Qwen/Qwen2.5-7B-Instruct`, device `cuda`, adapter `models/qwen7b_lora`
- Remote focused tests: `pytest tests/test_api.py tests/test_router.py` -> 22 passed.
- Remote compile: `python -m compileall app scripts` -> passed.
