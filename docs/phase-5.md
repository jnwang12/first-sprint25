# Phase 5 solution: Frontend → Backend Integration

This branch starts from `phase4` and connects the Next.js **Ask about Prad** button to the question-taking API. It logs the successful JSON response to the **browser console** and displays the answer on the page. The existing student tuple view remains available.

## Run both services

From the repository root:

```bash
source .venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Keep the existing Supabase and Gemini credentials in `backend/.env`. No provider key belongs in the frontend. The frontend's `NEXT_PUBLIC_API_URL` defaults to `http://localhost:8000`; the backend's `FRONTEND_ORIGIN` defaults to `http://localhost:3000`. If you change a port or use `127.0.0.1` in the browser, update these settings to match exactly and restart the services.

## See the response

1. Open `http://localhost:3000`.
2. Open browser DevTools and choose **Console** (not the terminal running Next.js).
3. Click **Ask about Prad**.
4. Wait for the request to finish. Expand the object following `[Phase 5] Agent API response:`.
5. In **Network**, inspect the `POST /api/agent/ask` request to see the JSON body, HTTP status, and response.

The request body is:

```json
{"question":"How many records in the database have a name of Prad?"}
```

An illustrative response is:

```json
{
  "question": "How many records in the database have a name of Prad?",
  "answer": "There are 3 records in the database with the name Prad.",
  "records_analyzed": 6,
  "tool_calls": 1
}
```

Counts and wording come from the live data and model. They are not hard-coded. Clicking invokes Gemini and can incur provider charges; loading the page does not invoke the agent.

## Follow the code

- `frontend/src/app/page.tsx` is a client component. Its click handler awaits the request, logs the parsed response using `console.log`, and updates the displayed answer.
- `frontend/src/lib/api.ts` sends JSON with `Content-Type: application/json` to the Phase 4 endpoint. `AgentAnswer` describes the response fields.
- FastAPI validates the body, awaits the Phase 3 tool-using agent, and returns JSON.
- While waiting, the button is disabled. A failed request is logged with `console.error` and shown on the page. A new attempt clears the previous answer/error.

To inspect a failure, stop the backend and click the button again. Expect a visible connection error and a console error rather than a successful response. Restart it to retry. CORS errors generally mean the browser origin differs from `FRONTEND_ORIGIN`.

This phase is a single button/request interaction. There is no chat input or conversation history yet; that belongs to Phase 6.

## Checks

From `frontend/`, run `npm run lint`, `npm run build`, and `npm run typecheck`. The Phase 4 API tests remain available with `python -m pytest -q` from the repository root.
