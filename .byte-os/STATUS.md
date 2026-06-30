Stage: delivered-v2
Current command: byte-auto
Next recommended command: capture V2 demo screenshots if final report needs real screenshots instead of placeholders

Summary:
- Project idea: Shenzhen MSU-BIT University admissions dialogue system for gaokao applicants and parents.
- Current recommendation: build a RAG-first assistant with structured score queries, source citations, multi-turn clarification, and evaluation.
- Server use: available later for model hosting, embedding/reranking, batch evaluation, or deployment.
- GitHub workflow target: local development -> GitHub push -> server pull/run -> capture evidence for report.
- Report target: Chinese academic report with Abstract, Introduction, Method, Result, and References using real citations.
- Delivery target confirmed: code + Web demo + LaTeX-compiled PDF report.
- Teacher emphasis confirmed: project completeness.
- Lightweight model training confirmed as an auxiliary component.
- Product code, data scripts, Web demo, tests, server deployment, evaluation, and report have been delivered for v0.
- V1 expands undergraduate/graduate admissions dimensions, repairs greeting/clarification behavior, runs local Qwen on the server, and includes subagent-guided QA fixes.

Open confirmations:
- none from user; current work proceeds under byte-auto.

Shaped artifacts:
- BYTE.md
- PRODUCT_SPEC.md
- UX_SPEC.md
- TECH_SPEC.md
- ROADMAP.md
- OKRS.md
- DECISIONS.md

Plans total: 7
Plans complete: 7/7
Ready plans:
- none

Pending plans:
- none

Verification:
- pytest: 22 focused V2 tests passed after subagent fixes; 28 full tests passed before final V2 fix set
- pytest final local: 29 passed
- compileall: passed for app and scripts
- ingestion: 13 documents, 10 fetched, 3 fallback
- training: accuracy 0.9375, macro-F1 0.8974
- evaluation: 58 questions, router accuracy 0.7586, source coverage 1.000
- LaTeX: report PDF compiled
- Qwen2.5-7B QLoRA: 960 SFT examples; 2 epochs; 210 steps; train loss 0.021; eval loss 0.022
- remote V2: `/api/qwen-health` reports Qwen/Qwen2.5-7B-Instruct on CUDA with `models/qwen7b_lora`; focused tests 22 passed
- local API smoke: greeting, clarification, exact undergraduate program, undergraduate enrollment boundary, graduate enrollment, and master list passed

Delivery remaining:
- none for V2. Optional: replace report demo placeholders with final browser screenshots and recompile.

GitHub:
- origin: https://github.com/elan6666/smbu-.git
- branch: main
- push: succeeded

Server:
- path: /data/yilangliu/smbu-admission-assistant
- port: 18080
- health: http://10.24.1.91:18080/api/health returned ok with qwen_configured=true
- Qwen service: http://127.0.0.1:18082 running Qwen/Qwen2.5-7B-Instruct on CUDA with `models/qwen7b_lora`
- remote pytest: 18 passed; targeted final smoke 11 passed after warning text patch
- remote training: accuracy 0.9375, macro-F1 0.8974
- remote evaluation: 58 questions, router accuracy 0.7586, source coverage 1.000
- remote smoke: greeting, clarification, undergraduate single学籍, undergraduate enrollment boundary, graduate enrollment, and Qwen health passed
- note: the final one-line warning text patch is committed locally/GitHub at 5856e42; server GitHub pull timed out, so the same line was applied directly on the server worktree before restart.
- V2 server update: code synced by rsync; Qwen2.5-7B QLoRA smoke and full training completed through `HF_ENDPOINT=https://hf-mirror.com`; adapter-backed Qwen service and Web backend are running.

Latest review:
- review-4 verdict: ship after V2 subagent findings, local tests, server training, server health, remote focused tests, and PDF compile.
