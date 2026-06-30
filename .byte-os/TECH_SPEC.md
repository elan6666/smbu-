# Tech Spec

## Architecture

```text
official web/PDF sources
        |
        v
crawler + document parser + table parser
        |
        +--> raw documents
        +--> cleaned chunks
        +--> structured score tables
        |
        v
embedding index + BM25 index + SQLite
        |
        v
retrieval + reranking + query router
        |
        v
Qwen-family generator with grounded prompt
        |
        v
FastAPI backend -> Web frontend
```

## Recommended Stack

- Backend: Python, FastAPI, Pydantic.
- Frontend: React or simple Vite app.
- Data crawling: `requests`, `beautifulsoup4`, optional `playwright` for dynamic pages.
- PDF/table extraction: `pypdf`, `pdfplumber`, `pandas`.
- Database: SQLite for structured admissions tables and metadata.
- Vector store: FAISS or Chroma for local/server simplicity.
- Retrieval: dense embedding plus lexical fallback.
- Reranking: Qwen3 reranker if feasible; otherwise a smaller cross-encoder or heuristic reranking.
- Generation: local/server Qwen-family instruct model through vLLM, Ollama, llama.cpp, or a compatible local API depending on server capability.
- Lightweight training: intent classifier or query router using labeled questions. Candidate models: logistic regression/SVM over embeddings, or a small transformer classifier if time allows.
- Report: LaTeX, BibTeX/BibLaTeX, PDF compiled by XeLaTeX or latexmk.

## Data Sources

Trusted source categories:

- SMBU admissions website.
- 2025 summer gaokao admissions regulation.
- admissions plan pages.
- major introduction pages.
- scholarship pages.
- school/campus-life official pages.
- employment/development official reports if available.

Lower-trust optional source category:

- student experience content, only if clearly labeled as non-official and excluded from policy/score answers.

## Data Model

`documents`
- `id`
- `title`
- `url`
- `source_type`
- `published_at`
- `fetched_at`
- `trust_level`
- `raw_path`
- `clean_text`

`chunks`
- `id`
- `document_id`
- `chunk_index`
- `text`
- `section_title`
- `embedding_id`

`admission_scores`
- `id`
- `year`
- `province`
- `category`
- `batch`
- `admission_mode`
- `major`
- `min_score`
- `min_rank`
- `source_url`
- `notes`

`qa_eval`
- `id`
- `question`
- `question_type`
- `expected_source`
- `expected_answer_points`
- `difficulty`

`intent_examples`
- `text`
- `label`
- `split`

## APIs

- `POST /api/chat`: main chat endpoint.
- `POST /api/search`: retrieve documents for debugging and evidence display.
- `GET /api/scores`: structured score lookup.
- `GET /api/sources`: list indexed sources.
- `POST /api/eval/run`: run evaluation set.
- `GET /api/health`: deployment health check.

## Query Routing

Question classes:

- `school_fact`
- `admission_policy`
- `score_query`
- `major_intro`
- `campus_life`
- `scholarship`
- `career`
- `comparison_or_advice`
- `unsupported`

Routing rules:

- Score queries must use SQLite first, then add explanatory RAG context if needed.
- Policy and major questions must require official-source retrieval.
- Advice questions must combine known user context with retrieved evidence and include uncertainty.
- Unsupported questions must refuse or ask for clarification.

## Grounded Generation Constraints

- Use retrieved evidence and structured rows only.
- Cite every factual claim with source IDs.
- If evidence is insufficient, say so.
- Do not infer unpublished admissions thresholds.
- Do not guarantee admission.

## Lightweight Training Plan

Purpose: show model-building work without weakening factual reliability.

Preferred training target:

- Intent/query-routing classifier trained on manually labeled admissions questions.

Dataset:

- 200-500 synthetic/manual questions based on real source categories.
- Train/dev/test split.
- Labels aligned with query classes above.

Evaluation:

- Accuracy and macro-F1.
- Confusion matrix.
- Error examples.

Integration:

- Use classifier output to choose score lookup, RAG retrieval, or clarification behavior.
- Keep a fallback rule-based router for reliability.

## Testing Strategy

- Unit tests for parsers, score lookup, router, and prompt assembly.
- Retrieval smoke tests for official source documents.
- End-to-end chat tests for representative questions.
- Evaluation script generating JSON/CSV results for report.
- Server smoke test: `/api/health`, one score query, one RAG answer.

## Implementation Risks

- Official pages may change layout; crawler needs source-specific parsers and saved raw snapshots.
- Score tables may be inconsistent across years/provinces.
- Qwen local deployment depends on server GPU/CPU resources.
- Reranker may be too heavy; keep a fallback.
- UI should not hide source evidence because evidence is a grading asset.

## Server Workflow

Target workflow:

```text
local edit -> local test -> git commit -> git push
server: git pull -> install/update env -> run backend/frontend/model -> capture logs/screenshots
```

Remote default data path: `/data/yilangliu`.

