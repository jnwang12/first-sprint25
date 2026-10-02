# Phase 1: Read data with Supabase

Learn the Supabase Python query syntax, then write your own query and print its results.
The connection setup is provided. All exercise code lives in `main.py`.

## Setup

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

## Read the example

`main.py` includes a query that reads the name and major of the student with
`id = 2` from the existing `students` table. It prints:

```text
[{'name': 'mac', 'major': 'ethics'}]
```

## Your task

Complete the TODO at the bottom of `main.py`:

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

Produce this output from the query results, rather than hard-coding the records.
You are done when your script prints all three tuples in this order.

## Branches

- `phase-1-base`: provided setup, a reference read query, and the TODO.
- `phase-1-solution`: the same files with the TODO completed.

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

- [Read queries](https://supabase.com/docs/reference/python/select)
- [Ordering results](https://supabase.com/docs/reference/python/order)
