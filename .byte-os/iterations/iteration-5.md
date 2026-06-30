# Iteration 5: Context-Aware Dialogue Repair

Date: 2026-07-01

## Evidence

- User screenshot showed failures for “人工智能怎么样”, “你是什么助手”, and “刚才我问了什么”.
- The assistant needed short session context, not long-term memory.

## Changes

- Added `app/context.py`.
- Added `history` to `/api/chat`.
- Frontend now sends recent chat history.
- Added direct context recall for previous question and previous assistant answer.
- Added program-pronoun resolution for “它/这个专业”.
- Tightened routing for assistant identity and known program questions.

## Verification

- Focused tests passed locally and remotely.
- API smoke:
  - `你是什么助手` returns identity response without sources.
  - `刚才我问了什么` returns the previous user question.
  - `人工智能怎么样` followed by `它是双学籍吗` resolves to artificial intelligence program facts.
