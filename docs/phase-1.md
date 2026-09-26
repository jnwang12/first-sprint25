# Phase 1: Supabase and Python

**Goal:** read the pre-made student table and print one `(name, email, major)` tuple per record. This guide provides setup, function contracts, hints, and checkpoints—not the implementation.

## 1. Use the provided table information

The workshop's supplied REST endpoint is:

```text
https://nmsxavnfdvsozgblaknt.supabase.co/rest/v1/students
```

For the Python client, set `SUPABASE_URL` to **`https://nmsxavnfdvsozgblaknt.supabase.co`**, without `/rest/v1/students`. The client uses the table name `students` when you implement the query. The instructor has confirmed the `students` table and the `name`, `email`, and `major` columns. The live table and its read permissions have not been queried by this scaffold.

Use this table contract:

| Setting | Expected value |
| --- | --- |
| Schema | `public` |
| Table | `students` |
| Columns to read | `name`, `email`, `major` (text) |
| Access | Read access using the supplied publishable or legacy anon key |

`db/seed.sql` is instructor setup for a fresh workshop database. It supplies nine fictional students, including three named Prad. Students should query the pre-made table, not run inserts or recreate it. If your instructor uses a different table, confirm its schema, exact table/column names, and read-access policy before coding. Expected row counts below apply only to the unchanged seed data.

## 2. Prepare Python

From the repository root, create an environment if you have not already:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
```

If `backend/.env` does not exist, copy `backend/.env.example` to it. Set `SUPABASE_URL` to the project URL and `SUPABASE_KEY` to the instructor-provided publishable or legacy anon key. Keep the file out of Git.

The frontend's `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` correspond to these two values, but Python reads **`backend/.env`**, not **`frontend/.env.local`**. Configuring the frontend alone does not configure Python. No OpenAI key, Next.js server, or FastAPI server is needed for Phase 1.

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and use `Copy-Item` to copy files.

## 3. Check configuration before writing the query

```bash
python -c "from backend.db_client import get_supabase_client; get_supabase_client(); print('Client created; table access has not been tested.')"
```

This checks that the client can be constructed from your settings. It does **not** prove the key is valid, that the table exists, or that rows are readable. Only your completed query will check database access. Do not print your key while debugging.

## 4. Complete the three extension points

Open `backend/exercise.py`. `TABLE_NAME` and `STUDENT_COLUMNS` are supplied so you can focus on the Python query rather than tracking down table names. Match the numbered TODOs to the steps below.

1. **`fetch_students(client)`**: build and execute a read query, then return the records. Keep printing out of this function so the later agent can reuse it.
2. **`to_student_tuple(record)`**: extract the three named fields in the order `name`, `email`, `major`, and return a tuple.
3. **`main()`**: obtain the supplied client, call your query function, loop through the records, and print each converted tuple. Replace the starter message with your implementation.

`StudentRecord` documents a row dictionary; `StudentTuple` documents the output shape. Type hints guide your editor but do not perform runtime validation. The two helper functions intentionally raise `NotImplementedError` until you replace their bodies. The starter `main()` does not call them yet.

### Hints, without the solution

- Look up table selection, column selection, execution, and response data in the [Supabase Python select reference](https://supabase.com/docs/reference/python/select).
- A query builder and the records returned by an executed query are different objects.
- A returned row is a dictionary. The output should be a tuple containing values, not column names.
- Do not rely on dictionary ordering to decide which value goes first.
- Preserve distinct records with the same name. Prad is intentionally repeated.
- Do not filter or count Prad yet; this phase prints all records.

### Practice tuple conversion without a database

`backend/fixtures/phase1_students.json` contains three fictional row dictionaries. It is practice input only, not a copy of the live table, a database seed, or a fallback for failed queries. The app does not load it automatically.

After implementing `to_student_tuple`, use Python's standard `json` module to load the fixture and try your function on each record. You write this small practice loop yourself.

Check these cases:

| Input characteristic | What your implementation should preserve |
| --- | --- |
| Fields appear in different dictionary orders | Output always follows `(name, email, major)` |
| Two records share the name Prad | Both records remain present with different emails |
| A list contains no records | No student tuples are produced |

For the first fixture record, the expected value is:

```text
('Prad', 'practice.prad.cs@example.com', 'Computer Science')
```

This lets you isolate Python conversion mistakes before debugging connectivity. Completing this practice does not complete Phase 1: the final script must read the pre-made Supabase table.

## 5. Run and inspect

From the repository root with your Python environment activated:

```bash
python -m backend.exercise
```

For the provided seed, one output line would look like:

```text
('Maya Chen', 'maya@example.com', 'Mechanical Engineering')
```

Row order is not part of the acceptance criteria. Do not hard-code this output; it must come from Supabase.

## Completion checklist

- The script reads the instructor's Supabase table without modifying it.
- Each returned row produces one three-item tuple in the requested field order.
- The unchanged seed produces nine records, including all three distinct Prad records.
- An empty result is handled clearly rather than replaced with fake data.
- Database failures remain distinguishable from an empty successful result.
- Querying, tuple conversion, and printing have separate responsibilities.
- Credentials are not printed or committed.

To check your tuple conversion independently, try a fictional row dictionary whose keys are written in a different order. Its tuple should still be ordered by name, email, and major. For query testing, compare your output with the instructor's Table Editor rather than assuming a fixed count for a modified dataset.

## Common problems

| Symptom | Check |
| --- | --- |
| Missing environment settings | Edit `backend/.env`; frontend settings are separate |
| Module import error | Activate `.venv` and run the module from the repository root |
| Invalid key or URL | Confirm both values refer to the same Supabase project |
| Table or column not found | Confirm schema and exact names with the instructor |
| No rows despite known data | Confirm project, filters, and row-level read policy with the instructor |
| `NotImplementedError` | A scaffold function still needs your implementation |
| Only the setup message appears | Wire your functions together in `main()` |

Do not disable row-level security to debug an empty result; ask the instructor to check the intended read policy. After completing Phase 1, commit your work and use it as the starting point for Phase 2.
