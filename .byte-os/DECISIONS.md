# Decisions

## D001: RAG-first architecture

Decision: Use retrieval-augmented generation as the core method.

Rationale: Admissions information changes over time and must be traceable to sources. RAG makes updates and citations easier than memorizing facts through fine-tuning.

## D002: Lightweight training only

Decision: Include lightweight model training for intent/query routing rather than factual fine-tuning.

Rationale: This satisfies the need for visible NLP/model work while keeping factual answers controlled by retrieval and structured data.

## D003: Structured score table

Decision: Store historical score data in SQLite/CSV tables, not only in a vector index.

Rationale: Score queries need exact filtering and table output. Vector retrieval alone is not reliable for numeric admissions questions.

## D004: Code + Web demo + LaTeX PDF

Decision: Deliver source code, a runnable Web demo, and a Chinese LaTeX report compiled to PDF.

Rationale: The teacher values project completeness; these outputs show engineering, NLP method, deployment, and academic communication.

## D005: GitHub and server workflow

Decision: Use GitHub as the source-of-truth repository and run the project on the server by pulling from Git.

Rationale: This keeps local development, remote execution, and submission evidence reproducible.

