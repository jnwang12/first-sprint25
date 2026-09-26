"""Phase 1 starter. Run from the repository root: python -m backend.exercise."""
from typing import TypedDict

from supabase import Client

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
    # TODO 1A: Choose TABLE_NAME using the supplied client.
    # TODO 1B: Select STUDENT_COLUMNS in the format the Supabase SDK expects.
    # TODO 1C: Execute the query and return the response's records.
    # An empty table should return an empty list, not invented sample data.
    raise NotImplementedError("Phase 1: implement the Supabase read query.")


def to_student_tuple(record: StudentRecord) -> StudentTuple:
    """Convert one record to (name, email, major), in that exact order."""
    # TODO 2: Access each named field and construct a three-item tuple.
    # Use explicit field names; do not depend on the dictionary's field order.
    # Practice input is available in backend/fixtures/phase1_students.json.
    raise NotImplementedError("Phase 1: implement the tuple conversion.")


def main() -> None:
    # TODO 3A: Import and call get_supabase_client from backend.db_client.
    # TODO 3B: Pass that client to fetch_students.
    # TODO 3C: Loop through the results and print each converted tuple.
    # TODO 3D: Give helpful feedback if there are no visible records.
    # Replace this setup message once you implement the steps above.
    print("Phase 1 starter ready. Follow docs/phase-1.md to complete the TODOs.")
    print("1. fetch_students: retrieve records from Supabase.")
    print("2. to_student_tuple: convert one record to (name, email, major).")
    print("3. main: connect, retrieve, convert, and print each record.")
    # Later: Phase 2 feeds records to the agent; Phase 3 moves retrieval into a tool.


if __name__ == "__main__":
    main()
