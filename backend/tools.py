"""Phase 3: read-only database access, executed only when the agent calls a tool."""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass

from pydantic_ai import RunContext

from backend.db_client import get_supabase_client
from backend.exercise import StudentRecord, fetch_students


class StudentLookupError(RuntimeError):
    """A database failure must not be treated as an empty dataset."""


def load_student_records() -> list[StudentRecord]:
    return fetch_students(get_supabase_client())


@dataclass
class StudentTools:
    # A fresh instance for every question; no records are loaded at construction.
    load_students: Callable[[], list[StudentRecord]] = load_student_records
    records_analyzed: int | None = None
    tool_calls: int = 0


async def get_student_names(ctx: RunContext[StudentTools]) -> list[dict[str, str]]:
    """Retrieve student names from Supabase. Each entry represents a separate record.

    Use this tool before answering questions about how many students have a name.
    It is read-only and retains duplicate names. It does not calculate the answer.
    """
    try:
        records = await asyncio.to_thread(ctx.deps.load_students)
        names = [{"name": record["name"]} for record in records]
    except Exception as exc:
        raise StudentLookupError("Unable to load student records from Supabase.") from exc
    ctx.deps.records_analyzed = len(names)
    ctx.deps.tool_calls += 1
    # Only the data needed for this question reaches the model.
    return names


async def get_students(ctx: RunContext[StudentTools]) -> list[StudentRecord]:
    """Read student names, emails, and majors for questions and follow-up questions.

    Each returned item is one database record. Duplicate names are separate students.
    This tool only reads data and cannot modify the database.
    """
    try:
        records = await asyncio.to_thread(ctx.deps.load_students)
        rows = [
            {"name": row["name"], "email": row["email"], "major": row["major"]} for row in records
        ]
    except Exception as exc:
        raise StudentLookupError("Unable to load student records from Supabase.") from exc
    ctx.deps.records_analyzed = len(rows)
    ctx.deps.tool_calls += 1
    return rows
