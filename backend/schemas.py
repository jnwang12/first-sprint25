"""Response contract for the student preview; agent contracts remain exercises."""
from pydantic import BaseModel


class StudentResponse(BaseModel):
    name: str
    email: str
    major: str


# TODO (Phase 4): Define request and response models for the agent endpoint.
# TODO (Phase 6): Extend the agent contract for conversation history.
