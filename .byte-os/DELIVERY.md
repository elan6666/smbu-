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

- `pytest`: 8 passed
- `python -m compileall app scripts`: passed
- `python scripts/ingest_sources.py --limit 8`: 7 documents, 5 fetched, 2 fallback
- `python scripts/train_intent.py`: accuracy 0.900, macro-F1 0.852
- `python scripts/evaluate_system.py`: 50 questions, router accuracy 0.760, source coverage 1.000
- LaTeX compile: passed
- Local Web smoke: `/api/health`, `/api/chat`, and `/` passed on port 8001

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
- Health response: `{"status":"ok","service":"smbu-admission-assistant"}`
- Server pytest: 8 passed
- Server training metrics: accuracy 0.900, macro-F1 0.852
- Server evaluation metrics: 50 questions, router accuracy 0.760, source coverage 1.000

Because the server's Ubuntu Python lacked `python3.12-venv`, deployment used:

```bash
python3 -m pip install --user virtualenv --break-system-packages
python3 -m virtualenv .venv
source .venv/bin/activate
```

## Current Risks

- Some source pages used fallback records because HTTP fetch failed.
- Current score table focuses on Guangdong rows; broader province coverage should be added if time allows.
- Retrieval is a lexical baseline; Qwen embedding/reranker integration is a v1 improvement.
