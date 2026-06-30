# UX Spec

## Core User Journey

1. User opens the Web demo.
2. User optionally fills applicant context: province, category, score/rank, preferred major.
3. User asks an admissions question in Chinese.
4. System classifies the question type: school facts, score query, major advice, campus life, policy, or unsupported.
5. System retrieves documents and/or queries structured score tables.
6. System answers with clear wording, source cards, and uncertainty notes.
7. User asks a follow-up question; the assistant reuses applicant context when appropriate.

## Screen List

- Chat page: main user surface.
- Source/evidence panel: shows retrieved documents, snippets, dates, and URLs.
- Score table view: shows province/year/category/major rows for admissions-score answers.
- About/data page: explains data sources, update date, and limitations.
- Evaluation page or report artifact: optional but useful for demoing test results.

## Navigation Model

- Single-page app is sufficient.
- Left or top area: applicant profile controls.
- Center: chat messages.
- Right or collapsible panel: sources and score tables.
- Header: project name and data-update status.

## Interaction Model

- The assistant should ask targeted clarification questions, not a long form.
- For score/risk questions, the assistant should first check whether province/category/rank are known.
- For factual answers, source cards should be visible by default or one click away.
- For missing data, show a short explanation and suggest what the user can ask instead.

## States

- Empty state: show several realistic applicant questions.
- Loading state: show retrieval/generation progress in concise text.
- Success state: answer + evidence + optional table.
- Partial state: answer from available sources with missing-data notice.
- Error state: plain-language error and retry option.
- Unsupported state: refusal with source boundary, not generic apology.

## First-Run Experience

Show example prompts:

- "广东物理类考生想报深北莫，应该先看哪些信息？"
- "2025 年普通高考录取模式有哪些专业？"
- "电子与计算机工程专业适合什么学生？"
- "宿舍和校园生活有哪些官方信息？"
- "我只有省份和分数，还缺什么信息才能判断报考风险？"

