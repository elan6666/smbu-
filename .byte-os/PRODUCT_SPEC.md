# Product Spec

## Positioning

This project is a Chinese admissions consultation assistant for Shenzhen MSU-BIT University. It combines retrieval-augmented generation, structured admissions-score querying, and a small Qwen-family language model to answer high-value questions from gaokao applicants and parents.

The goal is not to build a generic chatbot. The goal is to demonstrate a complete NLP system: data acquisition, cleaning, retrieval, reranking, answer generation, lightweight training, evaluation, deployment, and a reproducible academic report.

## Target Users

- Primary user: gaokao applicants considering Shenzhen MSU-BIT University.
- Secondary users: parents helping applicants compare majors, admission modes, dormitory/campus life, and school strengths.
- Course evaluator: teacher or teaching assistant checking system completeness, NLP method, demo quality, and report rigor.

## Problems And Jobs To Be Done

- Applicants need school-specific facts without reading many scattered pages.
- Applicants need historical score information by province, category, year, and major.
- Applicants need explanations of admission modes, professional options, language requirements, and degree/cultivation characteristics.
- Parents need trustworthy answers with clear sources rather than model-generated claims.
- Evaluators need to see that the system uses NLP methods, not only a UI around a large model.

## MVP

The v0 system must support:

- Chinese Web chat interface.
- User profile fields: province, subject category, score, rank, preferred major, and question history.
- Official-source document ingestion from Shenzhen MSU-BIT University admissions pages and related official pages.
- Structured admissions-score table ingestion and lookup.
- Hybrid retrieval: vector retrieval plus keyword/BM25 fallback where feasible.
- Reranking before generation.
- Qwen-family model or compatible local/server model for answer generation.
- Lightweight training component, preferably intent classification or query routing, with a small labeled dataset and evaluation.
- Evidence-grounded answers with source cards.
- Refusal/uncertainty behavior for unsupported or stale questions.
- Evaluation set with representative and adversarial questions.
- LaTeX report compiled to PDF.

## Non-Goals

- Do not train a large language model from scratch.
- Do not use fine-tuning as the main source of factual knowledge.
- Do not promise exact admission outcomes.
- Do not scrape private personal data.
- Do not build a multi-university platform before the SMBU system is complete.
- Do not fabricate references, metrics, screenshots, or deployment evidence.

## Functional Requirements

- Answer school overview, admissions policy, major, campus life, scholarship, and employment/development questions.
- Query historical admissions scores from structured data.
- Ask clarifying questions when province, category, year, or score/rank is missing.
- Return answer provenance for factual claims.
- Separate official sources from lower-trust sources if unofficial sources are later added.
- Save or export demo examples for the report.

## Quality Requirements

- Answers should be grounded in retrieved evidence or structured tables.
- The system should prefer "当前资料未覆盖" over hallucinated answers.
- Structured score answers should show table fields, not only prose.
- The demo should run reproducibly on the server.
- The report should use real references and visible experiment artifacts.

## Acceptance Criteria

- A user can open the Web demo, ask at least 10 representative admissions questions, and receive useful answers.
- Score-related questions trigger structured lookup rather than generic generation.
- At least 50 evaluation questions are stored and runnable.
- Evaluation output includes retrieval quality, answer faithfulness/manual correctness, and failure cases.
- The server run instructions are documented and verified.
- The LaTeX report compiles to PDF.

