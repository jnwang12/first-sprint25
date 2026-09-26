"""Query Supabase and print tuples. Run from the root: python -m backend.exercise."""
from typing import TypedDict, cast

from supabase import Client

from backend.db_client import get_supabase_client

# Provided table information. Use these when implementing your query.
TABLE_NAME = "students"
STUDENT_COLUMNS = ("name", "email", "major")


class StudentRecord(TypedDict):
    """The three columns confirmed for the workshop's students table."""

    name: str
    email: str
    major: str


StudentTuple = tuple[str, str, str]


def fetch_students(client: Client) -> list[StudentRecord]:
    """Return student records from Supabase, without printing or modifying them."""
    response = (
        client.table(TABLE_NAME)
        .select(",".join(STUDENT_COLUMNS))
        .execute()
    )
    return cast(list[StudentRecord], response.data)


def to_student_tuple(record: StudentRecord) -> StudentTuple:
    """Convert one record to (name, email, major), in that exact order."""
    return (record["name"], record["email"], record["major"])


def main() -> None:
    students = fetch_students(get_supabase_client())
    if not students:
        print("No student records are visible. Check the table and its read policy.")
        return

    for student in students:
        print(to_student_tuple(student))


if __name__ == "__main__":
    main()
