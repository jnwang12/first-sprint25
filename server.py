"""Phase 4: serve the Phase 3 student agent over HTTP."""

from threading import Lock
from uuid import UUID, uuid4

from pydantic_ai.messages import ModelMessage

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from main import student_agent

app = FastAPI(title="Workshop Student Agent")

# Phase 5 setup: allow the local Next.js app to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


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


# Phase 6 setup: each chat gets its own history, including tool calls/results.
class ChatQuestion(AgentQuestion):
    conversation_id: UUID | None = None


class ChatAnswer(AgentAnswer):
    conversation_id: UUID


# Workshop-only memory: restart/reload clears chats; use one server process.
conversations: dict[UUID, list[ModelMessage]] = {}
conversation_lock = Lock()

# TODO (Phase 6):
# 1. Register POST /api/agent/chat with response_model=ChatAnswer.
# 2. Use request.conversation_id or create a new ID with uuid4().
# 3. Inside `with conversation_lock:`, load that chat's history (default []).
# 4. Call student_agent.run_sync(request.question, message_history=history).
# 5. Save result.all_messages() under the ID only after a successful run.
# 6. Return ChatAnswer(answer=result.output, conversation_id=conversation_id).
# Keep /api/agent/ask as the previous stateless Phase 4/5 reference.
