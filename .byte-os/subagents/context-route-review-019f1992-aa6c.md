# V2 Subagent Review: Context And Routing

Subagent: `019f1992-aa6c-7fe3-a96b-4447012bd2f3`

Mode: read-only review

## Scope

- `/api/chat` history handling.
- Context recall for “刚才我问了什么”.
- Pronoun follow-up for “它/这个专业”.
- Major-routing behavior for `人工智能怎么样`.

## Findings

1. If the frontend sends history that already contains the current user message, “刚才我问了什么” can incorrectly recall the current question rather than the previous question.
2. Exact program questions can be polluted by broad keyword matching, causing unrelated program rows to appear in responses.

## Fixes Applied

- `app/context.py` now skips the current question when looking for the previous user message.
- `app/main.py` filters exact program rows before broad program matching is allowed.
- Added regression tests:
  - `test_context_recalls_previous_question_when_history_contains_current_message`
  - `test_major_intro_for_ai_program`

## Verification

- Local focused tests: 22 passed.
- Remote focused tests: 22 passed.

## Verdict

Ship after fixes.
