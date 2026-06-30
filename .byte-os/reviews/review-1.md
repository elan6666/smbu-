# Review 1

Date: 2026-06-30

Verdict: iterate

## Findings

- P1: Server deployment is not yet verified. Local demo works, but project delivery requires remote run evidence.
- P2: Two official source pages used fallback records due HTTP errors. This is acceptable for demo continuity but should be disclosed.
- P2: Structured score table is useful but currently Guangdong-focused. Broader province coverage remains future work.
- P3: Retrieval is lexical rather than embedding-based. This is acceptable for v0 but should be described as a baseline.

## Passing Checks

- Tests pass.
- Training and evaluation scripts run.
- PDF compiles.
- Local API and Web demo respond.

## Required Iterations

- Core completeness: replace placeholder score data with real rows.
- UX/onboarding: make Web demo usable with profile fields and example prompts.
- Delivery readiness: add README, PDF, Git/server workflow, and delivery notes.

