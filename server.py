"""Phase 4: serve the Phase 3 student agent over HTTP."""

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from main import student_agent

app = FastAPI(title="Workshop Student Agent")


class AgentQuestion(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=1)


class AgentAnswer(BaseModel):
    answer: str


# Reference: a route that returns JSON without calling the agent.
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Solution (Phase 4):
# 1. Register a POST route at /api/agent/ask with response_model=AgentAnswer.
# 2. Write a regular def handler accepting request: AgentQuestion.
# 3. Call student_agent.run_sync(request.question).
# 4. Return AgentAnswer(answer=result.output).
# Let the existing agent call get_students; do not query Supabase in this route.
# Use regular def with run_sync, rather than calling run_sync inside async def.


@app.post("/api/agent/ask", response_model=AgentAnswer)
def ask_agent(request: AgentQuestion) -> AgentAnswer:
    result = student_agent.run_sync(request.question)
    return AgentAnswer(answer=result.output)
