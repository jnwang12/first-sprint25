# Phase 6: Chatbot

Replace the fixed-question button with a chatbot. Goal: have a conversation with
the agent about records in the student database, including follow-up questions.

## What is provided

- Completed Phase 1–5 code. The Phase 5 button remains at `/button`.
- A chatbot page at `/` with an input form, message list, loading/error handling,
  and a **New chat** control.
- Backend chat request/response models, a conversation history dictionary, and a
  lock for sequential history updates.
- TODOs in `server.py` and `frontend/app/page.js`.

**The base is starter code:** submitting the form displays your message locally
and logs it in the browser console. It does not call the agent, and
`/api/agent/chat` is not implemented yet. The solution completes both TODOs.

## Run locally

Use your existing Phase 5 environment and backend `.env`. From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload
```

Keep that terminal open. In a second terminal, use Node.js 22 or newer:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`. No new dependencies or keys are needed.
Use frontend port 3000 so it matches the backend's CORS settings.

For a fresh checkout, use Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Fill in `SUPABASE_KEY` and `GEMINI_API_KEY`. Keep the workshop Supabase URL and
use a Gemini model available to your account. The workshop key needs SELECT access
to `public.students`. Keep all keys in the backend `.env`, which is ignored by Git.
On PowerShell, activate with `.venv\Scripts\Activate.ps1` and copy with
`Copy-Item .env.example .env`.

## Your task: backend

Complete the TODO in `server.py`:

1. Register `POST /api/agent/chat` with `response_model=ChatAnswer`.
2. Accept `request: ChatQuestion` in a regular `def` handler.
3. Use `request.conversation_id` or generate a new ID with `uuid4()`.
4. Inside `with conversation_lock:`, load that ID's history from `conversations`,
   defaulting to an empty list.
5. Call `student_agent.run_sync(request.question, message_history=history)`.
6. After a successful run, save `result.all_messages()` under the conversation ID.
7. Return the agent's answer and conversation ID in a `ChatAnswer`.

Use the full Pydantic AI message history. It includes tool requests and database
results as well as the conversation text. A visible chat transcript alone does
not give the model context. Keep histories separate by ID and save only after a
successful run. Keep `/api/agent/ask` as the stateless earlier-phase endpoint.

## Your task: frontend

Complete the TODO inside `sendMessage` in `frontend/app/page.js`:

1. POST JSON `{ question, conversation_id: conversationId }` to `API_URL`.
2. Set `Content-Type: application/json` and check `response.ok`.
3. Parse the returned JSON and save `data.conversation_id` with `setConversationId`.
4. Append `{ role: "assistant", content: data.answer }` with a functional
   `setMessages` update so the user's message is retained.

The supplied code already adds the user message, clears the input, disables the
form while loading, and restores the input/transcript if a request fails.
**New chat** clears the transcript and ID; the next request starts fresh.

## Verify the solution

1. Ask: `How many records have the name prad?`
2. Confirm the answer appears in an agent message and the backend prints
   `Tool called: get_students`. With the unchanged workshop data, there are 3.
3. Follow up: `What majors do those records have?` Confirm it refers to the
   records from the previous question and uses database facts.
4. Inspect Developer Tools → Network: both POSTs to `/api/agent/chat` should use
   the same conversation ID (the first request sends null; the response supplies it).
5. Click **New chat** and ask another question. Confirm a new ID is returned.
6. Open a second tab and start a chat. Confirm it receives its own ID and history.

The answer wording may vary. Do not hard-code the count, answers, or database
records. Every turn uses provider quota. The Phase 5 `/button` example should
continue to work independently.

Request and response contract:

```json
{"question":"How many records have the name prad?","conversation_id":null}
```

```json
{"answer":"There are 3 records with the name prad.","conversation_id":"<UUID returned by the server>"}
```

Use the returned UUID for later questions. Empty questions or invalid IDs return
HTTP 422. If the request fails, the page shows an error; inspect the backend
traceback for database or model issues. In the base, the chat endpoint returns 404.

History lives in one Python process and clears on server restart or reload.
Use one Uvicorn worker for this workshop. The simple lock serializes chat runs.
Refreshing the page starts a new chat; old histories remain in server memory until
restart. Unknown valid IDs start an empty history. Durable storage, authentication,
streaming, and history cleanup are outside this exercise.

Check the frontend build with `cd frontend` followed by `npm run build`.

## Branches

```text
phase-5-solution
└── phase-6-base
    └── phase-6-solution
```

- `phase-6-base`: previous solutions, chat UI scaffolding, history setup, and TODOs.
- `phase-6-solution`: the same files with chat requests and conversation history implemented.

## References

- [Pydantic AI message history](https://ai.pydantic.dev/message-history/)
- [Next.js client components](https://nextjs.org/docs/app/api-reference/directives/use-client)
