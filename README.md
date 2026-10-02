# Phase 1: Read and write with Supabase

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

## Read the two examples

`main.py` includes a read query and a write query against the existing `students` table:

1. Read the name and major of the student with `id = 2`.
2. Update that student's major to `ethics` and return their name and major.

The update writes the current value, so it can be repeated without adding rows or
changing the expected dataset. Both examples print:

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

- `phase-1-base`: provided setup, two reference queries, and the TODO.
- `phase-1-solution`: the same files with the TODO completed.

## Instructor preparation

Use the existing `public.students` table with `id`, `name`, `email`, and `major`.
No seed or table creation is needed. Expected output comes from the table screenshot
provided on October 2, 2026; confirm the records still match before the workshop.

The provided key needs SELECT access for the exercise and UPDATE access to `major`
on the example row (`id = 2`). The old repository seed allowed reads only, so check
the current table grants and row-level policies before distributing this exercise.
Use a workshop key with those limited permissions; do not distribute a service-role
or secret key or disable row-level security to make the example work.

Both reference queries should return the row shown above. If an example returns
`[]` or a permission error, check the project, row, and access policies before asking
students to debug their own query.

## API reference

- [Read queries](https://supabase.com/docs/reference/python/select)
- [Update queries](https://supabase.com/docs/reference/python/update)
- [Ordering results](https://supabase.com/docs/reference/python/order)
