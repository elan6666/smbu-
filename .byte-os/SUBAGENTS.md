# Subagents

Auto mode permits subagents, but this initial build uses sequential execution because the first implementation touches shared app/data/report contracts. Safe future subagent slices:

- Data parsing review: inspect `scripts/ingest_sources.py`, `data/sources.json`, and processed documents.
- Report review: inspect `report/main.tex`, references, and generated metrics.
- Server smoke check: inspect deployment commands and `/api/health` output.

No actual subagents were started in this pass.

