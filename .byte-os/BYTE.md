# SMBU Admissions Dialogue System

## Project

Chinese NLP course final project: a Shenzhen MSU-BIT University admissions dialogue system for gaokao applicants and parents.

## Product Promise

Help prospective applicants ask concrete admissions questions and receive evidence-grounded answers with source citations, structured score lookup, and clear uncertainty boundaries.

## Delivery Target

- Runnable Web demo.
- Source code hosted in GitHub repository `https://github.com/elan6666/smbu-.git`.
- Server deployment workflow: local development -> GitHub push -> server pull/run.
- Chinese academic report compiled from LaTeX to PDF.
- Lightweight model training or adaptation as an auxiliary experiment, not the core factual memory mechanism.

## Working Principles

- Prefer official school/admissions sources over unofficial content.
- Store admissions score data in structured tables, not only vector embeddings.
- Use retrieval-augmented generation for factual answers.
- Cite the sources used for each factual response.
- Do not claim admission certainty; report risk and missing data explicitly.

