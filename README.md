# Phase 4: API Endpoint

Start a server with an endpoint that invokes the Phase 3 student agent. The goal
is to answer the same database question using curl or Postman instead of running
a Python script.

## Setup

Use your Phase 3 environment and `.env`. Install the updated dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For a fresh checkout, use Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Fill in `SUPABASE_KEY` and `GEMINI_API_KEY` in `.env`. The workshop Supabase URL and
Gemini model name are already supplied. Use a model available to your account.
Get a Gemini key from [Google AI Studio](https://aistudio.google.com/apikey).
Keep `.env` out of Git. The key needs SELECT access to `public.students`.

On Windows PowerShell, use `py -m venv .venv`, activate with
`.venv\Scripts\Activate.ps1`, and copy with `Copy-Item .env.example .env`.

## What is already provided

- `main.py`: the completed Phase 1–3 code, including `student_agent` and its
  `get_students` tool. Script examples now run only with `python main.py`, so
  importing the agent does not execute database queries or model calls.
- `server.py`: a FastAPI app, a complete health endpoint, JSON request and response
  models, the imported student agent, and the Phase 4 TODO.
- `requirements.txt`: previous dependencies plus FastAPI and Uvicorn.

The request model accepts a nonblank `question`; the response model contains an
`answer`. Each request starts a fresh agent run. Model calls use your provider quota
and may incur charges.

## Start the server

Run from the repository root:

```bash
python -m uvicorn server:app --reload
```

`server:app` means the `app` object in `server.py`. Uvicorn serves it at
`http://127.0.0.1:8000`; `--reload` reloads the server when you save code.
Stop it with Ctrl+C. Keep this terminal open and use a second terminal for curl.

Try the provided reference endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.
The base has only the health route; the agent route appears after you implement it.
The environment variables must be filled in before starting either branch because
importing `main.py` configures the Supabase client and Gemini model.

## Your task

Complete the TODO at the bottom of `server.py`:

1. Register `POST /api/agent/ask`, using `response_model=AgentAnswer`.
2. Create a handler with a parameter typed as `AgentQuestion`.
3. Send `request.question` to the existing `student_agent` with `run_sync`.
4. Return `AgentAnswer` with the result's `output` as its `answer`.

Use a regular `def` handler. FastAPI runs it in a worker thread, where the
synchronous `run_sync` call can wait for the agent. Do not put `run_sync` inside
an `async def` handler. The existing agent should retrieve records through its
`get_students` tool; keep database queries out of the endpoint.

## Test with curl

After completing the TODO, run this in a second terminal:

```bash
curl -X POST http://127.0.0.1:8000/api/agent/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many records have the name prad?"}'
```

Expected response (wording may vary):

```json
{"answer":"There are 3 records with the name prad."}
```

The server terminal should print `Tool called: get_students`. Confirm both that
the tool ran and that the answer matches the database. The count assumes the
workshop records are unchanged. The HTTP response contains the answer, not the
script's earlier example output.

Try sending `{"question":""}` or `{}` instead. FastAPI should return HTTP 422
for an invalid request without running the agent. Before the TODO is complete,
the agent URL returns HTTP 404.

On Windows PowerShell, use `curl.exe` for the curl commands; put the POST command
on one line instead of using Bash's backslash continuation.

## Test with Postman

1. Create a **POST** request to `http://127.0.0.1:8000/api/agent/ask`.
2. Select **Body → raw → JSON**; confirm `Content-Type: application/json`.
3. Enter `{"question":"How many records have the name prad?"}`.
4. Click **Send** and check for HTTP 200 and an `answer` in the JSON response.

If the server cannot start, check your active environment and `.env` settings.
If `/health` works but the agent request fails, check the server traceback,
provider key/model, and Supabase read access. A GET request to the completed agent
route returns HTTP 405; use POST with a JSON body.

## Branches

```text
phase-3-solution
└── phase-4-base
    └── phase-4-solution
```

- `phase-4-base`: completed earlier phases, server setup, a health reference, and the TODO.
- `phase-4-solution`: the same files with the agent endpoint implemented.

## References

- [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI synchronous and asynchronous handlers](https://fastapi.tiangolo.com/async/)
- [Pydantic AI agent runs](https://ai.pydantic.dev/agents/)
