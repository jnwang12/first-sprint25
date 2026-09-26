"""Response contracts for the student preview and Phase 4 agent API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class ChatMessage(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(AgentQuestion):
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def complete_exchanges(self):
        if len(self.history) % 2:
            raise ValueError("History must contain complete user/assistant exchanges.")
        for index, message in enumerate(self.history):
            expected = "user" if index % 2 == 0 else "assistant"
            if message.role != expected:
                raise ValueError("History must alternate user and assistant messages.")
        return self
