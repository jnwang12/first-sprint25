# Phase 5: FE → BE Integration

Build a very small Next.js app that calls the completed Phase 4 backend from a
button. Goal: click the button, invoke the student agent, and print the JSON
response in the **browser console**.

## What is already provided

- The completed Phase 1–4 Python code and `POST /api/agent/ask` endpoint.
- Local CORS setup in `server.py` allowing the frontend on port 3000.
- A minimal Next.js App Router app in `frontend/` using JavaScript.
- A client page with a button, the question, backend URL, loading/error states,
  and a TODO in `frontend/app/page.js`.

The base button prints `Button clicked:` and the question. It does **not** call
the backend yet. The Phase 5 solution adds the request and logs the response.
Completed earlier phases belong in both branches.

## Start the backend

From the repository root, use your Phase 4 environment and `.env`:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload
```

For a fresh checkout, first create the environment with Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Fill in `SUPABASE_KEY` and `GEMINI_API_KEY`; keep the provided Supabase URL and
use a Gemini model available to your account. Keep `.env` out of Git. The workshop
key needs SELECT access to `public.students`. No new backend dependencies or keys
are required for Phase 5.

On Windows PowerShell, use `py -m venv .venv`, activate with
`.venv\Scripts\Activate.ps1`, and copy with `Copy-Item .env.example .env`.

Confirm the backend works before starting the frontend:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/agent/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many records have the name prad?"}'
```

Expected: `{"status":"ok"}` for health and an `answer` for the agent request.
Exact answer wording may vary. On PowerShell, use `curl.exe` and put the POST
command on one line.

## Start the frontend

Use Node.js 22 or newer. Keep the backend running and open a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`. Open Developer Tools → **Console**, then click
**Ask agent**. In the base, you should see the provided click message.
The answer is intended for the browser console, not the terminal running Next.js.

Use port 3000 so the frontend matches the backend's allowed origins. If Next.js
picks another port because 3000 is occupied, stop that process or update
`allow_origins` in `server.py`. Both `localhost:3000` and `127.0.0.1:3000` are allowed.

## Your task

Complete the TODO in `frontend/app/page.js`, inside `askAgent`:

1. Use `fetch(API_URL, ...)` to send a **POST** request.
2. Set `Content-Type` to `application/json`.
3. Set the body to `JSON.stringify({ question: QUESTION })`.
4. Check `response.ok` and throw an `Error` for a failed HTTP response.
5. Await `response.json()` and print the returned object with `console.log`.

Replace the reference click log with your implementation. Keep the provided
loading/error handling. `"use client"` enables the button's browser event handler
and React state. The request should happen only when the button is clicked.

The page calls the Python API directly; no Next.js API route or database client
is needed. Keep Gemini and Supabase keys in the backend `.env`, never in frontend
code. The hard-coded local API URL and question are provided for this exercise.

## Verify the solution

Click **Ask agent** with the browser console open. Expected console object:

```json
{"answer":"There are 3 records with the name prad."}
```

The answer comes from the API; do not hard-code it. The count assumes the workshop
records are unchanged. In Developer Tools → **Network**, verify a POST to
`http://127.0.0.1:8000/api/agent/ask` with the JSON question and HTTP 200. A CORS
preflight OPTIONS request may also appear. The backend terminal should print
`Tool called: get_students`.

While the request runs, the button shows `Asking…` and is disabled. If it fails,
the page displays an error and logs it in the console. If you see `Failed to fetch`,
check that the backend is running and the frontend origin matches CORS setup.
For HTTP 500, inspect the backend traceback and provider/database settings.
Each click starts a fresh agent run and uses your provider quota.

To check the frontend production build:

```bash
cd frontend
npm run build
```

## Branches

```text
phase-4-solution
└── phase-5-base
    └── phase-5-solution
```

- `phase-5-base`: completed earlier phases, local CORS setup, a Next.js button
  reference, and the fetch/console TODO.
- `phase-5-solution`: the same files with the button's API request implemented.

## References

- [Next.js installation and App Router](https://nextjs.org/docs/app/getting-started/installation)
- [Next.js client components](https://nextjs.org/docs/app/api-reference/directives/use-client)
- [FastAPI CORS setup](https://fastapi.tiangolo.com/tutorial/cors/)
