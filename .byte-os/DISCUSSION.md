# Discussion

Date: 2026-06-30

## User Request

Build an NLP course final project: a Shenzhen MSU-BIT University admissions dialogue system for prospective students and parents. The user wants to discuss how to get a high score before implementation, including whether to use a local small Qwen model with fine-tuning, RAG, or server-side deployment.

Follow-up request on 2026-06-30:
- Connect the local project to `https://github.com/elan6666/smbu-.git`.
- Use this workflow: develop locally, push code to GitHub/server, run the application on the remote server.
- Complete the course project end to end, including data crawling, model/RAG construction, system demo, and Chinese report writing.
- Report style should be serious and academic, with sections similar to Abstract, Introduction, Method, Result, and References.
- Use Nature-style writing/citation skills later to reduce "AI-like" prose and keep references real.

Confirmed follow-up on 2026-06-30:
- Use the recommended RAG-first direction.
- Include light model training as an auxiliary component.
- Teacher values project completeness.
- Final delivery should include code, a Chinese LaTeX report compiled to PDF, and a Web demo.

## Current Understanding

- The product should answer questions about Shenzhen MSU-BIT University for gaokao applicants and families.
- Core topics include school overview, province or region admission scores, majors, strengths, dormitory environment, campus life, and applicant concerns.
- The project should show NLP substance, not only a plain chatbot wrapper.
- The user has access to a remote server and may use it later for model hosting, data processing, or evaluation.
- The safest high-score direction is a RAG admissions assistant with structured score querying, citations, multi-turn clarification, and answer reliability controls.
- The GitHub repository appears suitable as the remote origin for this empty local project; local `git remote -v` is currently empty.
- The project should produce both a runnable system and a polished Chinese academic report.
- The report submission format is LaTeX -> PDF.

## Recommended Technical Direction

Primary recommendation: RAG first, not fine-tuning first.

Reasons:
- Admissions data changes every year; RAG can update documents and tables without retraining.
- Fine-tuning a small model on limited scraped school data is likely to teach style but not guarantee factual correctness.
- Course grading usually rewards a complete system: data collection, retrieval, answer generation, evaluation, UI, and error handling.
- A local or server-hosted Qwen model can still be used as the generator, but the knowledge should come from retrieved official sources and structured tables.

Suggested stack:
- Data ingestion: official school/admissions pages, enrollment brochures, admission score tables, major introductions, dormitory and campus-life sources.
- Structured layer: normalized CSV/SQLite tables for province, year, subject category, batch, major, lowest score, lowest rank when available.
- Retrieval layer: vector store for unstructured documents plus keyword/BM25 backup.
- Model layer: Qwen instruct model for generation, Qwen embedding/reranker model if feasible.
- Backend: FastAPI service with `/chat`, `/search`, `/score-query`, and `/sources`.
- Frontend: simple applicant-facing chat UI with source cards and score-table answers.

Recommended engineering workflow:
- Local machine: write code, run unit tests, build sample data, prepare report drafts.
- GitHub: source-of-truth repository and version history.
- Server: pull the latest GitHub code, build environment, run ingestion/embedding/model service, and host the demo.
- Deployment loop: local change -> local smoke test -> commit -> push GitHub -> server pull -> server run -> capture screenshots/logs for report.

Recommended report structure:
- Abstract: concise problem, method, system, and result summary in Chinese.
- Introduction: gaokao information asymmetry, school-specific admissions consultation need, and limitations of generic chatbots.
- Method: data acquisition, document cleaning, structured score database, retrieval, reranking, Qwen-based generation, prompt constraints, and evaluation design.
- Result: system screenshots, example questions, retrieval evidence, structured score answers, evaluation metrics, and failure analysis.
- References: only real official sources and real academic/model references; no fabricated citations.

## High-Score Product Features

- Applicant profile memory: province, subject category, score/rank, preferred major, language preference.
- Clarifying questions: ask for missing province/year/category before giving admission probability.
- Structured score answer: return tables/charts for historical cutoffs instead of vague prose.
- Evidence citations: every factual answer cites source title, URL/file, and retrieval snippets.
- Refusal and uncertainty handling: clearly say when data is missing or outdated.
- Evaluation set: 50-100 test questions covering school facts, majors, score queries, campus life, and adversarial questions.
- Demo scenarios: "广东物理类多少分能报", "计算机类有什么优势", "宿舍怎么样", "中外合作有什么特点", "我的位次适合哪些专业".
- Reproducible server demo: one command or documented commands to start backend/frontend/model service.
- Report figures: architecture diagram, data pipeline, retrieval example, UI screenshot, and evaluation table.

## Open Questions

Must confirm:
- Final delivery format: web app demo, notebook demo, command-line demo, or all three?
- Course grading emphasis: NLP algorithm, engineering system, UI/product completeness, or written report?
- Required language: Chinese only, bilingual Chinese/English, or optional Russian/English answers?
- Data scope: only official sources, or also include student forum/social-media material with lower trust labels?
- GitHub branch convention: use `main` directly or a `codex/*` feature branch first?

Nice to confirm:
- Whether the teacher expects model training/fine-tuning as a visible component.
- Whether admission probability should be conservative explanation only, or include a numeric risk score.
- Whether the project should support only SMBU or compare with similar universities.
- Report length and format: Word/PDF/Markdown/LaTeX, page limit, and whether screenshots are required.

## Suggested Defaults

- Build a Chinese-first RAG assistant with structured admissions tables.
- Use official sources as trusted knowledge; label unofficial material separately if used.
- Avoid full fine-tuning in the MVP; add optional LoRA fine-tuning only for intent classification or answer style if time remains.
- Use server resources later for running Qwen, embeddings, reranking, batch evaluation, or deployment.
- Include an evaluation report because it makes the system look like an NLP project rather than a normal app.
- Use GitHub as the remote origin and keep server deployment reproducible from Git rather than manually copying edited files.
- Write the final report in Chinese academic prose; use Nature-style skills later for structure, citation checks, and language polishing.
- Include light model training through intent/query routing rather than factual fine-tuning.

## Confirmed Decisions

- Discussion phase only; no product code started yet.
- Byte OS project state has been initialized only for discussion tracking.
- Recommended path is RAG-first with optional local/server Qwen model, not data-scrape fine-tuning as the core method.
- Target deliverable is now system plus Chinese academic report.
- Workflow target is local development, GitHub synchronization, server deployment, and evidence capture for the report.
- Delivery format is confirmed as code + Web demo + LaTeX-compiled PDF report.
- Project completeness is the main grading emphasis.
- Lightweight model training is accepted as an auxiliary experiment.

## Non-Goals For MVP

- Do not train a large model from scratch.
- Do not promise exact admission outcomes.
- Do not rely on hallucinated school facts.
- Do not scrape sensitive personal data.
- Do not build a large multi-school admissions platform unless the single-school version is already complete.

## Risks

- Admission scores and policies are time-sensitive; sources must be timestamped and refreshable.
- Some official pages may be PDF-heavy or table-heavy, requiring PDF/table extraction cleanup.
- Student-life answers from unofficial sources may be noisy and subjective.
- Local small models may hallucinate if retrieval and answer constraints are weak.
- Fine-tuning on tiny scraped data can reduce general ability and still fail on factual updates.
- A report that claims model training or evaluation without real experiments will be weak; every result should come from logs, screenshots, or saved evaluation files.
- References must be verified at writing time; placeholder citations are not acceptable.

## Recommended Next Command

`$byte-plan` after confirming Git branch/deployment preference and report length if available.
