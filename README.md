# first-sprint26

A workshop starter for learning **Python, Supabase, Pydantic AI, FastAPI, Next.js, and TypeScript** across six phases.

**Phase 1 is implemented; Phases 2–6 remain scaffolding.** The Python script queries Supabase and prints student tuples. Students implement the agent, tools, API endpoint, frontend request, and chatbot next. The starter includes dependencies, environment configuration, a Supabase client factory, a Next.js student preview, and FastAPI health and read-only student endpoints. There is no directory app, local database integration, or phase solution.

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

Check [the health endpoint](http://localhost:8000/health) or [FastAPI docs](http://localhost:8000/docs). `/health` is only a setup check. `GET /api/students` serves the Phase 1 records to the frontend. Students create the separate agent endpoint in Phase 4.

### Frontend (a separate terminal)

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

Open [localhost:3000](http://localhost:3000). The page displays live student tuples from `GET /api/students`, with loading, error, empty, and refresh states. Keep FastAPI running in the other terminal and configure `backend/.env`. The agent button and chatbot remain later exercises.

Both servers can start without credentials, but the student preview and Phase 1 script require Supabase settings. Model access becomes necessary in Phase 2.

## Supabase setup

The instructor prepares a Supabase project and runs `db/seed.sql` in its SQL editor before Phase 1. It creates a `students` table with `id`, `name`, `email`, `major`, and `created_at`, and nine fictional records, including three named Prad. Re-running the seed does not duplicate its records.

Students put the project URL and **publishable key or legacy anon key** in `SUPABASE_URL` and `SUPABASE_KEY` in `backend/.env`. `backend/db_client.py` provides `get_supabase_client()` as connection plumbing; it does not query anything. The seed permits reading this fictional dataset with row-level security and does not grant anonymous writes. Do not use its public-read policy for real student data.

For Phase 2 onward, configure `OPENAI_API_KEY` for a provider model available to your account. Model calls can incur charges. All provider credentials belong in `backend/.env`, never in frontend code or a `NEXT_PUBLIC_` variable.

## Frontend Supabase helpers

The frontend includes `@supabase/supabase-js` and `@supabase/ssr` as optional session plumbing. Configure `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` in `frontend/.env.local` (see `.env.example`). Use only a publishable key here. This file is ignored by Git; restart Next.js after editing it.

- `src/utils/supabase/client.ts`: browser client factory.
- `src/utils/supabase/server.ts`: server client factory accepting `await cookies()`.
- `src/utils/supabase/middleware.ts`: session-refresh helper.
- `src/proxy.ts`: Next.js 16 entry point that runs the helper and forwards refreshed cookies and cache headers.

The proxy skips refresh when Supabase settings are absent so a fresh workshop checkout still starts. When configured, it calls `getClaims()` to refresh existing sessions. It does not enforce login or protect routes. See [Supabase's SSR guide](https://supabase.com/docs/guides/auth/server-side/creating-a-client?framework=nextjs).

The student preview queries Supabase through Python/FastAPI, not the frontend Supabase helpers. Login UI is not included. Phase 5 adds the separate agent interaction. The optional Supabase agent-skills installer is not part of this setup.

## The six phases

| Phase | Students implement | Goal |
| --- | --- | --- |
| 1 — Supabase and Python | Query the pre-made student table | Print names, emails, and majors as tuples |
| 2 — Pydantic AI and Prompting | Inject retrieved records into an agent prompt | Ask how many records have the name Prad |
| 3 — Tool Calls | Let the agent retrieve data using a tool | Answer the same question through a tool call |
| 4 — API Endpoint | Expose the agent through FastAPI | Invoke it using curl or Postman |
| 5 — FE → BE Integration | Add a Next.js button that calls the endpoint | Print the response in the browser console |
| 6 — Chatbot | Replace the button with a conversational UI | Have a conversation about the database |

Start with the [Phase 1 guide](docs/phase-1.md) for Python setup, table details, and the implemented data flow. See [docs/workshop.md](docs/workshop.md) for all six phases and acceptance criteria. Phase 1 is complete and includes a read-only frontend preview. Agent-related goals in Phases 2–6 remain unimplemented.

## Where students work

```text
backend/
  config.py         Environment loading (provided)
  db_client.py      Supabase client factory (provided)
  exercise.py       Implemented Phase 1 query and tuple output
  agent.py          TODOs for prompting, tool registration, and history
  tools.py          TODOs for database tool calls
  schemas.py        Student response model; agent contract TODOs
  main.py           Student endpoint and CORS; agent endpoint TODO
  tests/            Health and offline Phase 1 tests
frontend/src/
  app/page.tsx      Student tuples with refresh, loading, and errors
  app/layout.tsx    Root layout and metadata
  app/globals.css   Minimal starter styles
  lib/api.ts        Typed student fetch; agent integration remains an exercise
db/seed.sql         Instructor-provided database preparation
```

## Branch workflow

Keep a clean starter commit as the common starting point. Students can create their own sequential branches, for example `student/<name>/phase-1` through `student/<name>/phase-6`, branching each phase from their previous work. An instructor can separately maintain checkpoint branches for workshops where learners start at a later phase.

Branch names are suggestions; the template does not create branches or include checkpoint implementations. Instructors should distribute starter branches separately from any solution branches.

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

The backend checks cover server health and Phase 1 behavior with offline data. Frontend checks verify scaffolding. Add behavior tests as later phases are implemented. GitHub Actions runs the same checks without Supabase or model credentials.

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
