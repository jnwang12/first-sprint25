# Phase 1: Supabase and Python

Phase 1 is implemented in `backend/exercise.py`. It reads `name`, `email`, and `major` from the pre-made Supabase `students` table and prints each record as a tuple. Phases 2–6 remain exercises.

## Run it

From the repository root, with dependencies installed:

```bash
source .venv/bin/activate
python -m backend.exercise
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

Configure `backend/.env` with the project base URL and the instructor-provided publishable or legacy anon key:

```dotenv
SUPABASE_URL=https://nmsxavnfdvsozgblaknt.supabase.co
SUPABASE_KEY=your-publishable-key
```

The REST endpoint is `https://nmsxavnfdvsozgblaknt.supabase.co/rest/v1/students`, but the Python client takes the base project URL, without the REST path. Python reads `backend/.env` independently of `frontend/.env.local`. No OpenAI key or running frontend/backend server is required.

## View records in the frontend

Start FastAPI from the repository root in one terminal:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`. The page fetches `GET /api/students` from FastAPI, which reuses `fetch_students`. Each record is displayed in tuple notation with quoted values. Use **Refresh records** to reload the live data. The view reports empty results and connection errors. This endpoint only reads records; it does not invoke an agent.

## Follow the code

1. `get_supabase_client()` loads the configured client.
2. `fetch_students(client)` selects the three columns and returns the response's row dictionaries.
3. `to_student_tuple(record)` extracts values in the explicit order `(name, email, major)`.
4. `main()` prints each tuple, or displays a message when no rows are visible.

For a fictional record, output looks like:

```text
('Maya Chen', 'maya@example.com', 'Mechanical Engineering')
```

Output comes from the live table, not the fixture or seed file. Duplicate names remain separate records, and row order is not guaranteed. The live database may differ from the nine-row repository seed. The query is read-only and does not create or modify records.

`StudentRecord` and `StudentTuple` provide editor type hints; they do not validate database results at runtime. The query uses Supabase's configured response-size limit, which is sufficient for this small workshop table. A larger dataset would need pagination.

## Verify and explore

```bash
python -m pytest backend/tests/test_exercise.py -q
```

Tests use fictional records from `backend/fixtures/phase1_students.json` and a mock client. They check tuple field order, preservation of duplicate names, empty results, and query failures without contacting Supabase.

Read the [Supabase Python select reference](https://supabase.com/docs/reference/python/select), then trace the data from the returned dictionaries into the printed tuples. Reuse `fetch_students` in Phase 2 when supplying data to your agent.

## Troubleshooting

- **Missing settings:** configure `backend/.env`, not only the frontend environment.
- **Import error:** activate the virtual environment and run the module from the repository root.
- **Invalid URL/key:** confirm both belong to the same project.
- **Missing table/column:** the expected table is `public.students`, with `name`, `email`, and `major`.
- **Empty result:** confirm the table contains rows and the key's read policy permits access. Do not disable row-level security.
- **Query failure:** errors propagate rather than being disguised as empty results; check the terminal error and connectivity.
