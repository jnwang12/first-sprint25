"""Response contracts for the student preview and Phase 2 answer."""
from pydantic import BaseModel


class StudentResponse(BaseModel):
    name: str
    email: str
    major: str


class PradAnswer(BaseModel):
    question: str
    answer: str
    records_analyzed: int


# Phase 4 can generalize the fixed Phase 2 question into a request model.
# TODO (Phase 6): Extend the agent contract for conversation history.
