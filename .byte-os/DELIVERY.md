# Delivery

Date: 2026-06-30

## Deliverables

- Web demo: FastAPI app serving `frontend/index.html`.
- Backend: `app/`
- Data and scripts: `data/`, `scripts/`
- Tests: `tests/`
- Report source: `report/main.tex`
- Submit-ready PDF: `report/smbu-admission-dialogue-report.pdf`

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_sources.py --limit 8
python scripts/train_intent.py
python scripts/evaluate_system.py
uvicorn app.main:app --reload --port 8000
```

If port 8000 is occupied:

```bash
uvicorn app.main:app --reload --port 8001
```

## Verification Summary

- `pytest`: 18 passed
- `python -m compileall app scripts`: passed
- `python scripts/ingest_sources.py --limit 20`: 13 documents, 10 fetched, 3 fallback
- `python scripts/train_intent.py`: accuracy 0.9375, macro-F1 0.8974
- `python scripts/evaluate_system.py`: 58 questions, router accuracy 0.7586, source coverage 1.000
- LaTeX compile: passed
- Local API smoke: greeting, clarification, exact undergraduate program, undergraduate enrollment boundary, graduate enrollment, and master list passed

## Server Run

Target directory: `/data/yilangliu/smbu-admission-assistant`

```bash
cd /data/yilangliu
git clone https://github.com/elan6666/smbu-.git smbu-admission-assistant
cd smbu-admission-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_sources.py --limit 8
python scripts/train_intent.py
python scripts/evaluate_system.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Verified server deployment:

- Path: `/data/yilangliu/smbu-admission-assistant`
- Running port: `18080`
- Health URL: `http://10.24.1.91:18080/api/health`
- Current v0 health response was previously verified. V1 server redeploy and smoke are pending in the current auto loop.

Because the server's Ubuntu Python lacked `python3.12-venv`, deployment used:

```bash
python3 -m pip install --user virtualenv --break-system-packages
python3 -m virtualenv .venv
source .venv/bin/activate
```

## Optional Local Qwen

The backend supports a local Qwen/OpenAI-compatible endpoint through:

```bash
export QWEN_API_URL=http://127.0.0.1:18082/v1/chat/completions
export QWEN_MODEL=Qwen/Qwen2.5-0.5B-Instruct
```

The helper service is:

```bash
pip install -r requirements-qwen.txt
python scripts/serve_qwen_openai.py --model Qwen/Qwen2.5-0.5B-Instruct --host 127.0.0.1 --port 18082
```

If `QWEN_API_URL` is not set, `/api/health` reports `qwen_configured=false` and the app uses deterministic grounded generation.

When Qwen is configured, the backend still skips Qwen rewriting for structured admissions facts such as scores, degree mode, teaching language, certificates, and enrollment counts. This keeps the local model connected without letting it alter official table values.

Current v1 status: backend hook and helper service exist. The server must report `qwen_configured=true` before the final handoff claims Qwen is actively connected.

## Current Risks

- Some source pages used fallback records because HTTP fetch failed.
- Current score table focuses on Guangdong rows; broader province coverage should be added if time allows.
- Retrieval is a lexical baseline; Qwen embedding/reranker integration is a v1 improvement.
