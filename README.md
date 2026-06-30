# SMBU Admissions Dialogue System

面向高考考生和家长的深圳北理莫斯科大学报考问答系统。项目采用 RAG-first 路线：官方数据抓取、结构化分数线查询、轻量意图分类训练、证据检索和 Web demo。

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

分数线等数值信息进入结构化表，政策和专业介绍进入文档检索。回答生成只基于检索片段和结构化查询结果，不把微调模型作为事实记忆来源。

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

