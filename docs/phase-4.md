# Phase 4 solution: API Endpoint

`phase4` builds on the tool-using agent from `phase3`. The primary interface is now **POST `/api/agent/ask`**: send a JSON question and receive the agent's answer. The earlier `/api/agent/prad` endpoint remains available so the existing frontend continues to work.

## Start the server

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Keep this terminal running. Configure `SUPABASE_URL`, `SUPABASE_KEY`, and `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in `backend/.env`. `GEMINI_MODEL` is optional. Restart after environment changes. No frontend or standalone agent script is needed to use this API.

## Invoke with curl

In a second terminal:

```bash
curl --fail-with-body --max-time 60 \
  -X POST http://localhost:8000/api/agent/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many records in the database have a name of Prad?"}'
```

On Windows PowerShell, use `curl.exe` or send the same request in Postman.

Example JSON response (wording and counts depend on the model and live data):

```json
{
  "question": "How many records in the database have a name of Prad?",
  "answer": "There are 3 records with the name Prad.",
  "records_analyzed": 6,
  "tool_calls": 1
}
```

## Invoke with Postman

Import [phase4.postman_collection.json](phase4.postman_collection.json), or create a request manually:

1. Select **POST** and enter `http://localhost:8000/api/agent/ask`.
2. Select **Body → raw → JSON**.
3. Enter `{"question":"How many records in the database have a name of Prad?"}`.
4. Click **Send** and inspect the JSON response and HTTP status.

The collection uses a `baseUrl` variable defaulting to `http://localhost:8000`. No provider keys belong in Postman: the server loads them from its environment. Each valid agent request may incur Gemini usage charges.

## Explore the contract

Open `http://localhost:8000/docs` for interactive FastAPI documentation or `http://localhost:8000/openapi.json` for its schema.

- `question` is required, trimmed, and must contain 1–500 characters.
- Unknown JSON fields are rejected.
- Questions about student names use the registered database tool, not preloaded data.
- Each request has independent tool state. This endpoint has no conversation history yet.
- The existing tool returns names only; questions requiring email or major data are outside its current capability.

| HTTP status | Meaning |
| --- | --- |
| `200` | Agent answer and actual tool metadata |
| `422` | Invalid request body; model is not invoked |
| `502` | Provider/agent failure, including failure to use the tool |
| `503` | Missing configuration or database lookup failure |
| `504` | Agent run exceeded the 45-second deadline |

The server accepts the request in `backend/main.py`, validates it using `AgentQuestion` in `backend/schemas.py`, and awaits `answer_question` in `backend/agent.py`. The database remains behind the Phase 3 tool. Errors return a public message without internal exception details.

This remains a local workshop server with no authentication or rate limiting. Add both before public deployment.

## Verify

```bash
python -m pytest -q
```

Phase 4 tests verify input validation, question forwarding, response serialization, and failure status codes with no provider calls. Earlier tests continue checking real tool-loop execution using a local model.
