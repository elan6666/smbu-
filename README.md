# SMBU Admissions Dialogue System

面向高考考生和家长的深圳北理莫斯科大学报考问答系统。项目采用 RAG-first 路线：官方数据抓取、结构化分数线查询、轻量意图分类训练、证据检索、本地 Qwen 角色提示词调优、日常对话和 Web demo。

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/ingest_sources.py --limit 8
python scripts/train_intent.py
python scripts/evaluate_system.py
uvicorn app.main:app --reload --port 8000
```

打开 `http://127.0.0.1:8000` 体验 Web demo。

## Repository Layout

- `app/`: FastAPI 后端、检索、路由、分数线查询、回答生成。
- `scripts/`: 数据抓取、轻量训练、系统评测脚本。
- `data/`: 数据源清单、结构化分数线、训练集、评测集。
- `frontend/`: 静态 Web demo。
- `report/`: 中文 LaTeX 报告。
- `.byte-os/`: Byte OS 项目管理、计划、评审和交付记录。

## Design

分数线等数值信息进入结构化表，政策和专业介绍进入文档检索。回答生成只基于检索片段和结构化查询结果，不把微调模型作为事实记忆来源。系统也支持受控联网搜索：用户勾选“联网搜索官方网页”或问题包含“最新/联网/现在”等词时，后端会搜索深北莫官方域名并把结果追加为证据。

## Web Search

联网搜索不需要额外 API key。后端使用 `/api/web-search?q=...` 查询官方域名结果，并在 `/api/chat` 中通过 `enable_web_search=true` 启用。

## Server Workflow

```bash
cd /data/yilangliu
git clone https://github.com/elan6666/smbu-.git smbu-admission-assistant
cd smbu-admission-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_sources.py --limit 8
python scripts/train_intent.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Optional Local Qwen

The app is RAG-first and works without a local LLM. To enable local Qwen generation, start an OpenAI-compatible Qwen service and point the backend to it. Structured facts such as scores, certificates, degree mode, teaching language, and enrollment counts are still answered by deterministic table logic so the model cannot rewrite numbers incorrectly:

```bash
pip install -r requirements-qwen.txt
python scripts/serve_qwen_openai.py --model Qwen/Qwen2.5-0.5B-Instruct --host 127.0.0.1 --port 18082
export QWEN_API_URL=http://127.0.0.1:18082/v1/chat/completions
export QWEN_MODEL=Qwen/Qwen2.5-0.5B-Instruct
uvicorn app.main:app --host 0.0.0.0 --port 18080
```

`/api/health` returns `qwen_configured=true` only when `QWEN_API_URL` is set.

`/api/qwen-health` checks whether the local Qwen process is actually reachable and reports the model/device when available.
