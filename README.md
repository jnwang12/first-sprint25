# first-sprint26

A workshop starter for learning **Python, Supabase, Pydantic AI, FastAPI, Next.js, and TypeScript** across six phases.

**This branch is scaffolding, not a completed app.** Students implement the database query, agent, tools, API endpoint, frontend request, and chatbot themselves. The starter includes dependencies, environment configuration, a Supabase client factory, a static Next.js page, and a FastAPI health check. There is no directory app, local database integration, or phase solution.

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

The exercise entry point prints a setup message. It does not query a database or invoke a model. On Windows PowerShell, create the environment with `py -m venv .venv`, activate with `.venv\Scripts\Activate.ps1`, and use `Copy-Item` instead of `cp`.

### Backend server

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check [the health endpoint](http://localhost:8000/health) or [FastAPI docs](http://localhost:8000/docs). `/health` is only a setup check. Students create the agent endpoint in Phase 4.

### Frontend (a separate terminal)

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

Open [localhost:3000](http://localhost:3000). The starter page makes no backend requests. Students add a button in Phase 5 and a chatbot UI in Phase 6.

Both servers and the starter script run without credentials. Database and model access become necessary when students implement the relevant phases.

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

The starter page remains unchanged: no table queries, login UI, or phase solutions are included. The workshop's database exercises still run through Python, and Phase 5 still connects the frontend to FastAPI. The optional Supabase agent-skills installer is not part of this setup.

## The six phases

| Phase | Students implement | Goal |
| --- | --- | --- |
| 1 — Supabase and Python | Query the pre-made student table | Print names, emails, and majors as tuples |
| 2 — Pydantic AI and Prompting | Inject retrieved records into an agent prompt | Ask how many records have the name Prad |
| 3 — Tool Calls | Let the agent retrieve data using a tool | Answer the same question through a tool call |
| 4 — API Endpoint | Expose the agent through FastAPI | Invoke it using curl or Postman |
| 5 — FE → BE Integration | Add a Next.js button that calls the endpoint | Print the response in the browser console |
| 6 — Chatbot | Replace the button with a conversational UI | Have a conversation about the database |

Start with the [Phase 1 guide](docs/phase-1.md) for Python setup, table details, and scaffold checkpoints. See [docs/workshop.md](docs/workshop.md) for all six phases and acceptance criteria. None of these phase goals are implemented in the starter.

## Where students work

```text
backend/
  config.py         Environment loading (provided)
  db_client.py      Supabase client factory (provided)
  exercise.py       CLI entry point with Phase 1–3 TODOs
  agent.py          TODOs for prompting, tool registration, and history
  tools.py          TODOs for database tool calls
  schemas.py        TODOs for the API request/response contract
  main.py           Server and CORS setup; agent endpoint TODO
  tests/            Setup smoke test; add tests alongside each phase
frontend/src/
  app/page.tsx      Static page; button and chatbot TODOs
  app/layout.tsx    Root layout and metadata
  app/globals.css   Minimal starter styles
  lib/api.ts        API URL only; request and TypeScript contract TODOs
db/seed.sql         Instructor-provided database preparation
```

## Branch workflow

`main` is the workshop starter, with setup, guided TODOs, and no phase solutions. Start your own work from `main`; the numbered branches are cumulative solution references, not starter branches for the next exercise.

| Branch | Contents |
| --- | --- |
| `main` | Starter template and Phase 1 scaffold |
| `phase1` | Completed Phase 1, including the student tuple frontend preview |
| `phase2`–`phase6` | Reserved for solutions through the matching phase; not created yet |

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

The health test and frontend checks verify scaffolding only, not completion of the phases. Add behavior tests as each phase is implemented. GitHub Actions runs the same checks without Supabase or model credentials.

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
