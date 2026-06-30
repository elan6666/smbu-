# AGENTS Audit

## Root AGENTS.md Status

Status: ready

Reason: includes purpose, start files, repo map, commands, safe edit boundaries, navigation, and maintenance.

## Module AGENTS.md Files

None. Current repository size does not justify local context files.

## Scoped Command Coverage

- Backend/API: `pytest tests/test_api.py`, `python -m compileall app`
- Data/RAG: `pytest tests/test_rag.py tests/test_scores.py`
- Training/router: `pytest tests/test_router.py`, `python scripts/train_intent.py`
- Evaluation/report: `python scripts/evaluate_system.py`, LaTeX compile for `report/main.tex`

## Noise Path Coverage

Generated paths are documented in `AGENTS.md`, `.gitignore`, and `.claude/settings.json`.

## LSP Coverage

Python LSP recommended. Static frontend does not need a local language-server setup.

## Subagent Boundary Coverage

Suggested boundaries: data parsing, report review, server smoke check.

## Proposed Updates

Add module-local `AGENTS.md` only if backend or report grows substantially.

## Last Reviewed

2026-06-30

## Next Review

2026-09-30

