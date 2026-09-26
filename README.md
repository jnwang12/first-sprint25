# first-sprint26

A workshop starter for learning **Python, Supabase, Pydantic AI, FastAPI, Next.js, and TypeScript** across six phases.

**All six phases are implemented on this solution branch.** Python queries Supabase and prints student tuples. A Pydantic AI agent retrieves names through a read-only tool and answers the Prad-count question, with a chatbot showing replies and lookup metadata. Follow-up questions use the current tab's recent conversation history. The starter includes dependencies, environment configuration, a Supabase client factory, a Next.js student preview, and FastAPI health and read-only student endpoints. There is no directory app, local database integration, or phase solution.

The checkout directory may still be called `first-sprint25`; that does not affect these commands.

## Local setup

Use **Node.js 22** (see `.nvmrc`) and **Python 3.11+**. Run commands from the repository root unless shown otherwise.

### Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
cp backend/.env.example backend/.env
python -m backend.exercise
```

The exercise entry point queries Supabase and prints each student as a tuple. Configure `backend/.env` as described below before running it. It does not invoke a model. On Windows PowerShell, create the environment with `py -m venv .venv`, activate with `.venv\Scripts\Activate.ps1`, and use `Copy-Item` instead of `cp`.

### Backend server

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check [the health endpoint](http://localhost:8000/health) or [FastAPI docs](http://localhost:8000/docs). `/health` is only a setup check. `GET /api/students` serves the Phase 1 records to the frontend. `POST /api/agent/ask` accepts a JSON question and returns an agent answer. `POST /api/agent/prad` remains compatible with the earlier frontend. See the [Phase 4 curl and Postman guide](docs/phase-4.md).

### Frontend (a separate terminal)

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

Open [localhost:3000](http://localhost:3000). The page displays live student tuples from `GET /api/students`, with loading, error, empty, and refresh states. Keep FastAPI running in the other terminal and configure `backend/.env`. The chat composer calls `/api/chat` with a message and recent history. Replies appear in the transcript and are logged in the browser console. See the [Phase 6 guide](docs/phase-6.md). Configure `GEMINI_API_KEY` in `backend/.env` to enable replies.

Both servers can start without credentials, but the student preview and Phase 1 script require Supabase settings. Model access becomes necessary in Phase 2.

## Supabase setup

The instructor prepares a Supabase project and runs `db/seed.sql` in its SQL editor before Phase 1. It creates a `students` table with `id`, `name`, `email`, `major`, and `created_at`, and nine fictional records, including three named Prad. Re-running the seed does not duplicate its records.

Students put the project URL and **publishable key or legacy anon key** in `SUPABASE_URL` and `SUPABASE_KEY` in `backend/.env`. `backend/db_client.py` provides `get_supabase_client()` as connection plumbing; it does not query anything. The seed permits reading this fictional dataset with row-level security and does not grant anonymous writes. Do not use its public-read policy for real student data.

For Phase 2 onward, configure `GEMINI_API_KEY` for a provider model available to your account. Model calls can incur charges. All provider credentials belong in `backend/.env`, never in frontend code or a `NEXT_PUBLIC_` variable.

## Frontend Supabase helpers

The frontend includes `@supabase/supabase-js` and `@supabase/ssr` as optional session plumbing. Configure `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` in `frontend/.env.local` (see `.env.example`). Use only a publishable key here. This file is ignored by Git; restart Next.js after editing it.

- `src/utils/supabase/client.ts`: browser client factory.
- `src/utils/supabase/server.ts`: server client factory accepting `await cookies()`.
- `src/utils/supabase/middleware.ts`: session-refresh helper.
- `src/proxy.ts`: Next.js 16 entry point that runs the helper and forwards refreshed cookies and cache headers.

The proxy skips refresh when Supabase settings are absent so a fresh workshop checkout still starts. When configured, it calls `getClaims()` to refresh existing sessions. It does not enforce login or protect routes. See [Supabase's SSR guide](https://supabase.com/docs/guides/auth/server-side/creating-a-client?framework=nextjs).

Both previews use Python/FastAPI; frontend Supabase helpers remain available for future auth work. Login UI is not included. The optional Supabase agent-skills installer is not part of this setup.

## The six phases

| Phase | Students implement | Goal |
| --- | --- | --- |
| 1 — Supabase and Python | Query the pre-made student table | Print names, emails, and majors as tuples |
| 2 — Pydantic AI and Prompting | Inject retrieved records into an agent prompt | Ask how many records have the name Prad |
| 3 — Tool Calls | Let the agent retrieve data using a tool | Answer the same question through a tool call |
| 4 — API Endpoint | Expose the agent through FastAPI | Invoke it using curl or Postman |
| 5 — FE → BE Integration | Add a Next.js button that calls the endpoint | Print the response in the browser console |
| 6 — Chatbot | Replace the button with a conversational UI | Have a conversation about the database |

Start with the [Phase 1 guide](docs/phase-1.md) for Python setup, table details, and the implemented data flow. See [docs/workshop.md](docs/workshop.md) for all six phases and acceptance criteria. All six phases are complete. See the [Phase 6 guide](docs/phase-6.md) for the chatbot, follow-up questions, and conversation reset. See [the Phase 3 solution guide](docs/phase-3.md) for setup and the tool-call flow. Use the [Phase 4 guide](docs/phase-4.md) to invoke the agent through curl or Postman.

## Where students work

```text
backend/
  config.py         Environment loading (provided)
  db_client.py      Supabase client factory (provided)
  exercise.py       Implemented Phase 1 query and tuple output
  agent.py          Tool-using agents for single questions and chat
  tools.py          Read-only name/full-record tools and per-run metadata
  chat.py           Convert bounded text history into model messages
  schemas.py        Student response model; agent contract TODOs
  main.py           Student and fixed-question agent endpoints
  tests/            Health, Phase 1, and offline agent/API tests
frontend/src/
  app/page.tsx      Chat transcript, composer, and student-data preview
  app/layout.tsx    Root layout and metadata
  app/globals.css   Minimal starter styles
  lib/api.ts        Typed student, agent, and chat requests
db/seed.sql         Instructor-provided database preparation
```

## Branch workflow

`main` is the workshop starter, with setup, guided TODOs, and no phase solutions. Start your own work from `main`; the numbered branches are cumulative solution references, not starter branches for the next exercise.

| Branch | Contents |
| --- | --- |
| `main` | Starter template and Phase 1 scaffold |
| `phase1` | Completed Phase 1, including the student tuple frontend preview |
| `phase2` | Completed Phases 1–2, with the prompt-based agent and frontend answer |
| `phase3` | Completed Phases 1–3, with database retrieval through a model tool call |
| `phase4` | Completed Phases 1–4, with a validated question-taking HTTP endpoint |
| `phase5` | Completed Phases 1–5, with a frontend button calling the API and logging its response |
| `phase6` | Completed Phases 1–6, with a conversational chatbot and per-tab history |

Create a personal working branch from `main`, implement each phase there, and consult the matching solution branch when ready. For example, `phase1` shows the Phase 1 answer; it is not the starting point for Phase 1. Future solution branches should include the earlier solutions they depend on.

Branches under `archive/` preserve the pre-reorganization history and are not workshop starting points or additional phase solutions.

## Checks

With the Python environment activated, from the root:

```bash
python -m ruff check backend
python -m pytest -q
```

From `frontend/`:

```bash
npm run lint
npm run build
npm run typecheck
```

The backend checks cover server health, Phase 1, the Pydantic AI tool pipeline, and the answer API with offline data. Frontend checks verify scaffolding. Add behavior tests as later phases are implemented. GitHub Actions runs the same checks without Supabase or model credentials.

## Troubleshooting

- Run Python entry points as modules from the root (`python -m backend.exercise`) so imports resolve.
- Restart a service after changing its environment file.
- For Phase 5, `NEXT_PUBLIC_API_URL` points to the backend, while `FRONTEND_ORIGIN` matches the browser origin exactly, including its port. Defaults use `http://localhost:8000` and `http://localhost:3000` respectively.
- If Supabase reads fail, check the project URL, key, seed, and table read policy.
- Keep model and database access in the backend. Authentication and deployment hardening are outside this local workshop starter.

## References

- [Next.js](https://nextjs.org/docs)
- [TypeScript](https://www.typescriptlang.org/docs/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase Python](https://supabase.com/docs/reference/python/introduction)
- [Pydantic AI](https://ai.pydantic.dev/)
