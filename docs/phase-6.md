# Phase 6 solution: Chatbot

`phase6` builds on `phase5`. The single-question button is replaced with a chat composer and a transcript. Users can ask about student names, emails, and majors, then refer to earlier answers in follow-up questions.

## Run

From the repository root, with Supabase and Gemini settings in `backend/.env`:

```bash
source .venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`. Try:

1. “How many students are named Prad?”
2. “What are their majors?”
3. “Which one studies computer science?”

Click **New chat** to clear the transcript and start without the previous context. Enter sends; Shift+Enter inserts a newline. Questions are limited to 500 characters. While a reply is pending, sending and resetting are disabled. On failure, the question is restored to the composer for retry; failed exchanges are not added to history.

## Conversation design

- The browser tab owns its transcript in React state. Reloading clears it; no local storage or database conversation storage is used.
- `POST /api/chat` receives `question` and the last ten completed exchanges as `history`.
- History permits only alternating user/assistant text messages, starting with a user and ending with an assistant. Limits: twenty historical messages, 8000 characters each, and a 500-character current question.
- `backend/chat.py` converts text into Pydantic AI `ModelRequest` and `ModelResponse` messages, passed through `message_history`.
- There is no shared server conversation state or global message list. Separate tabs cannot accidentally inherit each other's history. New chat sends an empty history.
- Older messages remain visible in the UI, but only the most recent ten exchanges are sent. References beyond that window may require the user to restate context.

The client-supplied transcript is context, not authorization or trusted database evidence. Previous tool calls/results are not accepted from the browser. Every reply must make a fresh lookup, and the output validator rejects answers without one.

## Database tools

The chat agent uses `get_students` from `backend/tools.py`, which reads `name`, `email`, and `major` and returns them to Gemini. This enables follow-ups about majors and email addresses. The earlier single-question endpoints still use the names-only tool, preserving the previous phases' behavior.

Tools are read-only. The current query is designed for the small workshop dataset and still uses Supabase's configured response-size limit. The agent cannot edit records, and its statements/counts are model-generated rather than independently verified database aggregations. Use workshop data; each message sends retrieved fields and recent conversation text to Gemini and may incur provider charges.

## API

```bash
curl --fail-with-body --max-time 60 \
  -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many students are named Prad?","history":[]}'
```

To follow up, send the previous user question and assistant answer in `history`:

```json
{
  "question": "What are their majors?",
  "history": [
    {"role": "user", "content": "How many students are named Prad?"},
    {"role": "assistant", "content": "There are 3 students named Prad."}
  ]
}
```

Use the actual answer returned to your first request rather than this illustrative answer. Responses retain `question`, `answer`, `records_analyzed`, and `tool_calls`. The frontend renders the answer as plain text and shows lookup metadata. Responses are logged in the browser console as `[Phase 6] Chat API response:`.

Error statuses remain `422` for invalid input, `503` for setup/database failures, `502` for agent/provider failures, and `504` for the 45-second run deadline. There is no streaming. Runs retain the three-model-request and two-tool-call limits.

## Code map and verification

- `frontend/src/app/page.tsx`: transcript, composer, loading/errors, reset, student-data preview.
- `frontend/src/lib/api.ts`: typed chat request and response handling.
- `backend/schemas.py`: bounded chat payload and transcript validation.
- `backend/chat.py`: conversion from text transcript to Pydantic AI history.
- `backend/agent.py`: separate chat instructions and tool selection, shared run logic.
- `backend/tools.py`: read-only full student-record tool.

Run `python -m pytest -q` from the root; from `frontend/`, run `npm run lint`, `npm run build`, and `npm run typecheck`. Offline chat tests verify a follow-up receives previous text, a new conversation receives no previous text, each turn retrieves fresh data, and malformed history cannot invoke the provider. The earlier phases' tests continue to run.

This remains a local workshop app. Add authentication, authorization, request limits, and appropriate data policies before exposing it publicly. Client-held history is intentionally simple and not a trusted server-side conversation archive.

[Pydantic AI message-history guide](https://pydantic.dev/docs/ai/core-concepts/message-history/)
