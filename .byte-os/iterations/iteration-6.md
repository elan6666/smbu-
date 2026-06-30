# Iteration 6: Qwen2.5-7B QLoRA Training

Date: 2026-07-01

## Evidence

- Earlier server runtime used a smaller Qwen model and did not provide real fine-tuning evidence.
- User asked for a real 7B training run with loss curves and report explanation.

## Changes

- Built 960 SFT examples covering assistant identity, context follow-up, program grounding, score guardrails, and future-score refusal.
- Added Qwen2.5-7B LoRA/QLoRA training script.
- Added adapter-aware Qwen OpenAI-compatible serving.
- Ran Qwen2.5-7B QLoRA on the server.

## Training Result

- Model: Qwen2.5-7B-Instruct.
- Method: QLoRA.
- Epochs: 2.
- Steps: 210.
- Final train loss: 0.021.
- Final eval loss: 0.022.
- Adapter: `models/qwen7b_lora`.

## Verification

- Server smoke training passed.
- Full training completed.
- Loss figure generated at `report/figures/qwen7b-lora-loss.png`.
- Server Qwen health reports 7B model and adapter.
