"""Response contracts for the student preview and Phase 4 agent API."""

from pydantic import BaseModel, ConfigDict, Field


class StudentResponse(BaseModel):
    name: str
    email: str
    major: str


class AgentQuestion(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    question: str = Field(
        min_length=1,
        max_length=500,
        examples=["How many records in the database have a name of Prad?"],
    )


class AgentAnswer(BaseModel):
    question: str
    answer: str
    records_analyzed: int
    tool_calls: int


# Keep the earlier preview contract compatible.
PradAnswer = AgentAnswer
# TODO (Phase 6): Extend the agent contract for conversation history.
