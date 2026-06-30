---
id: 002
title: Data Ingestion And RAG Core
status: complete
wave: 2
owner_role: Backend Engineer
depends_on: [001]
start_directory: .
context_files: [.byte-os/TECH_SPEC.md, .byte-os/PRODUCT_SPEC.md]
agents_context_stack: []
subagent_policy: none
---

# Goal

Build the official-source data pipeline and retrieval layer.

# OKR Link

KR1, KR2

# Scope

Official page crawling, document cleaning, chunking, SQLite storage, score seed data, and lexical retrieval fallback.

# Non-Goals

No broad unofficial crawling. No unsupported admission probability claims.

# Steps

## Step 1: Create source registry

- Purpose: Keep source provenance explicit.
- Actions:
  - Define trusted URLs and source categories.
  - Store fetched HTML snapshots and metadata.
- Files or modules:
  - `data/sources.yaml`
  - `scripts/ingest_sources.py`
  - `data/raw/`
- Expected output: Fetchable official source list.
- Step verification: Ingestion command writes `data/processed/documents.jsonl`.
- Subagent: none

## Step 2: Build document chunks and search index

- Purpose: Enable evidence-grounded answers.
- Actions:
  - Clean HTML to text.
  - Chunk documents.
  - Build TF-IDF/BM25-style lexical index as v0 fallback.
- Files or modules:
  - `app/rag.py`
  - `data/processed/`
- Expected output: Search returns source snippets.
- Step verification: `python scripts/ingest_sources.py --limit 5` then `/api/search` smoke test.
- Subagent: none

## Step 3: Add structured score table

- Purpose: Handle numeric admissions questions reliably.
- Actions:
  - Add schema and seed rows where verified data is available.
  - Query by province/category/year/major.
- Files or modules:
  - `app/database.py`
  - `data/structured/admission_scores.csv`
- Expected output: `/api/scores` returns rows or clear no-data response.
- Step verification: query one known row and one missing row.
- Subagent: none

# Dependencies

Plan 001.

# Scoped Commands

- Test: `pytest tests/test_rag.py tests/test_scores.py`
- Lint: not configured
- Typecheck: not configured
- Build: `python -m compileall app scripts`

# AGENTS.md Context

- Root context: none.
- Module context: none.
- Scoped command source: this plan.
- Safe edit boundaries: `app/`, `scripts/`, `data/`, `tests/`.
- Missing or stale AGENTS.md notes: none.

# Subagent Plan

None for v0.

# Code Change Guardrails

Store provenance with each document and table row.

# Acceptance Criteria

- Ingestion produces document records with title, URL, fetched time, and text.
- Search returns snippets with source IDs.
- Score lookup is structured and does not rely on generation.

# Verification

- `python scripts/ingest_sources.py --limit 5`
- `pytest tests/test_rag.py tests/test_scores.py`

# Experiment Or Measurement

Record indexed document count and chunk count.

# Risks

Official pages may be unavailable or encoded inconsistently.

# Notes

Dense embedding can be added after lexical retrieval works.
