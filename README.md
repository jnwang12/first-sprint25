# Phase 2: Ask an agent about database records

Learn to call Gemini through Pydantic AI, include database records in a prompt,
and print the answer. `main.py` keeps the completed Phase 1 code and adds the
provided agent setup, a reference call, and a Phase 2 TODO.

## Phase 2 setup

If you already completed Phase 1, activate your environment and install the updated dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Add these entries to your existing `.env`, keeping your Supabase settings:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey).
Use a model available to your account; the model name is configurable in `.env`.
Model calls use your provider account's quota and may incur charges.

If starting fresh, follow the Python setup below and fill in all four variables
from `.env.example`. Keep keys in `.env`, which is ignored by Git.

## Reference call

The provided code creates a Gemini-backed agent, asks it to reply with
`Hello from Gemini!`, and prints `result.output`.

`agent.run_sync(prompt)` waits for a completed response. `result.output` contains
the answer. The agent does not automatically have access to Supabase: your Python
code must include the retrieved records in the prompt.

## Phase 2 task

Complete the TODO at the bottom of `main.py`:

1. Query all students' names, emails, and majors. Retrieve all students, including
   those whose name is not `prad`.
2. Create a prompt containing those records and the question:
   "How many records have the name prad?"
3. Send that prompt to the agent.
4. Print the agent's answer.

Run everything from the repository root:

```bash
python main.py
```

The base prints the completed Phase 1 output followed by the greeting. The solution
also prints the answer to the database question. With the existing workshop records,
the answer should identify **3 records named prad**; the exact wording can vary.
Use the query results in your prompt rather than hard-coding the records or count.

## Branches

- `phase-2-base`: completed Phase 1, provided agent setup, a reference call, and the TODO.
- `phase-2-solution`: the same files with the Phase 2 TODO completed.

`phase-2-base` starts from the published `phase-1-solution`.
`phase-2-solution` branches directly from `phase-2-base`.

## Phase 1 reference

Learn the Supabase Python query syntax, then write your own query and print its results.
The connection setup is provided. All exercise code lives in `main.py`.

### Fresh Python setup

Use Python 3.11 or newer. From this repository's root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, use `py -m venv .venv`, activate with
`.venv\Scripts\Activate.ps1`, and copy with `Copy-Item .env.example .env`.

Put the instructor-provided workshop key in `SUPABASE_KEY` in `.env`.
The workshop project URL is already supplied. Keep `.env` out of Git.

Run the script:

```bash
python main.py
```

### Supabase reference query

`main.py` includes a query that reads the name and major of the student with
`id = 2` from the existing `students` table. It prints:

```text
[{'name': 'mac', 'major': 'ethics'}]
```

### Completed Phase 1 exercise

The supplied Phase 1 solution already does the following:

- Find every student whose name is exactly `prad` (lowercase).
- Retrieve their `name`, `email`, and `major`, ordered by `id`.
- Print one `(name, email, major)` tuple for each returned record.

**Hint:** a returned row is a dictionary. Access a specific field with `row["email"]`.

Expected output under `Your query:`, using the existing workshop records:

```text
('prad', 'joyfan123@gmail.com', 'computer science')
('prad', 'flashknight@rice.edu', 'aurafarming')
('prad', 'yoGurtYo@gmail.com', "i'm running out of ideas")
```

These values come from Supabase. Keep this completed exercise when adding Phase 2.

## Instructor preparation

Use the existing `public.students` table with `id`, `name`, `email`, and `major`.
No seed or table creation is needed. Expected output comes from the table screenshot
provided on October 2, 2026; confirm the records still match before the workshop.

The provided workshop key needs SELECT access to these records. Confirm the table
grants and row-level read policies before distributing the exercise.

The reference query should return the row shown above. If it returns
`[]` or a permission error, check the project, row, and access policies before asking
students to debug their own query.

## API reference

- [Pydantic AI agents](https://ai.pydantic.dev/agents/)
- [Using Gemini with Pydantic AI](https://ai.pydantic.dev/models/google/)
- [Read queries](https://supabase.com/docs/reference/python/select)
- [Ordering results](https://supabase.com/docs/reference/python/order)
