# Review 2

Date: 2026-06-30

Verdict: ship

## Findings

No blocking findings for course-project delivery.

## Evidence

- GitHub push succeeded on branch `main`.
- Server clone succeeded under `/data/yilangliu/smbu-admission-assistant`.
- Server virtual environment created with user-level `virtualenv` because Ubuntu lacked `python3.12-venv`.
- Server dependency install succeeded.
- Server ingestion succeeded: 7 documents, 4 fetched, 3 fallback.
- Server training succeeded: accuracy 0.900, macro-F1 0.852.
- Server evaluation succeeded: 50 questions, router accuracy 0.760, source coverage 1.000.
- Server pytest succeeded: 8 passed.
- Server compileall succeeded.
- Server FastAPI service started on port 18080.
- Local machine reached `http://10.24.1.91:18080/api/health` and received `{"status":"ok","service":"smbu-admission-assistant"}`.

## Residual Risks

- Some source pages fall back due remote fetch/SSL errors; source metadata is preserved and the report discloses this.
- Guangdong score rows are enough for the demo, but full national coverage remains a v1 extension.
- Retrieval is lexical baseline; embedding/reranker integration remains future work.

## Decision

Ship for the current course-project scope.

