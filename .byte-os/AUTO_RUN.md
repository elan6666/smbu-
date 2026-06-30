# Auto Run

Goal: Deliver the SMBU admissions dialogue system course project with Byte OS planning, implementation, server deployment, evaluation, Web demo, and a Chinese LaTeX PDF report.

Started at: 2026-06-30

## Current Loop

Terminal loop complete.

## Completed Stages

- byte-discuss
- byte-shape
- byte-plan
- byte-codebase-harness
- byte-build local waves 1-5
- local verification
- three iteration loops
- review 1
- GitHub push
- server deployment
- remote verification
- review 2
- iteration 4 local data/logic repair
- subagent-guided review 3
- Qwen server runtime
- remote smoke verification

## Remaining Plans

None.

## Review Verdict

Latest review: review-3. Initial subagent verdict was fail; fixes are complete and remote verification passed.

## Iteration Count

4

## Subagent Mode

on for v1 review. Two read-only subagents checked product/data readiness and code/API readiness.

## Hard Blockers

None.

## Exact Resume Action

No required action remains. Optional future work: broaden province score coverage, add dense embeddings/reranker, and record a demo video.
# Auto Run V2

Goal: Deliver the SMBU admissions assistant V2 with Qwen2.5-7B QLoRA fine-tuning evidence, multi-turn context support, updated report/PDF, placeholder demo screenshots, server deployment, Byte OS review/iterations, and final handoff.

Started at: 2026-07-01

Current loop number: 1

Completed stages:
- Existing Byte OS project detected.
- Codebase harness present.
- V2 plan created: `007-context-and-7b-finetune.plan.md`.

Remaining plans:
- 007 Context Memory And Qwen2.5-7B QLoRA Fine-Tuning.

Review verdict: pending

Iteration count: 0/3

Subagent mode: on for review/QA; main agent owns implementation and server training.

Hard blockers:
- none currently.

Exact resume action:
- Implement history/context schema, frontend history payload, routing fixes, SFT dataset/scripts, report updates, run verification, deploy and train on server.

## V2 Progress Update 2026-07-01 01:45 CST

Completed stages:
- Implemented `/api/chat.history` schema and frontend recent-history payload.
- Added context resolver for last-question recall, last-answer recall, and pronoun program follow-up.
- Added Qwen prompt history injection for non-structured evidence answers.
- Added SFT dataset builder with 960 examples: identity, context follow-up, program grounding, score guardrails, and future-score refusal.
- Added Qwen2.5-7B LoRA/QLoRA training script, training artifact writer, loss-figure writer, and adapter-serving support.
- Updated report to Qwen2.5-7B, LoRA/QLoRA, context pipeline, data-source table, and V2 screenshot placeholders.
- Ran local tests and report compile.
- Started server-side Qwen2.5-7B download/training smoke through `HF_ENDPOINT=https://hf-mirror.com`.

Subagent review:
- Context/router review found history compatibility and program-row pollution risks.
- Report/delivery review found premature completed-training wording and hardcoded training metadata.
- Fixes were applied and verified locally.

Verification:
- `pytest tests/test_api.py tests/test_router.py`: 22 passed.
- `python -m compileall app scripts`: passed.
- `tectonic -X compile report/main.tex --outdir report/build`: passed.
- Server data sync: passed.
- Server Qwen2.5-7B download: in progress, no GPU training yet.

Remaining plans:
- Finish 7B smoke, run longer LoRA/QLoRA training, copy training artifacts back, deploy adapter-backed Qwen, run API smoke, final review/delivery.

Review verdict: iterate until server training/deployment evidence is available.

Iteration count: 2/3

Exact resume action:
- Continue monitoring server model download; when smoke succeeds, start full training with the updated script and then redeploy Qwen 7B adapter.

## V2 Completion Update 2026-07-01

Completed stages:
- Finished Qwen2.5-7B smoke and full QLoRA training on the server.
- Copied training metrics and loss figure back into the report.
- Deployed adapter-backed Qwen2.5-7B service on `127.0.0.1:18082`.
- Restarted Web backend on `0.0.0.0:18080` with `QWEN_API_URL` pointing to the 7B service.
- Verified `/api/qwen-health` reports model `Qwen/Qwen2.5-7B-Instruct`, device `cuda`, adapter `models/qwen7b_lora`.
- Verified remote context, identity, program follow-up, score query, and evidence-generation smoke cases.
- Regenerated the PDF report with completed 7B training results.

Review verdict: ship.

Iteration count: 3/3

Subagent mode: completed for V2 review. Two read-only subagents checked context/routing and report/delivery claims; their blocking findings were fixed.

Hard blockers:
- none.

Exact resume action:
- No required V2 work remains. Capture the five demo screenshots listed in the final handoff and place them in `report/figures/`, then recompile the PDF if final visual screenshots are required instead of placeholders.
