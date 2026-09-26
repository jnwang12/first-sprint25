"""Phase 4: invoke the database agent over HTTP with a validated question."""

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend import config  # noqa: F401 -- loads backend/.env
from backend.agent import (
    AgentConfigurationError,
    answer_prad_question,
    answer_question,
    create_agent,
)
from backend.chat import answer_chat
from backend.db_client import get_supabase_client
from backend.exercise import fetch_students
from backend.schemas import AgentAnswer, AgentQuestion, ChatRequest, PradAnswer, StudentResponse
from backend.tools import StudentLookupError

app = FastAPI(title="First Sprint Workshop API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["setup"])
def health() -> dict[str, str]:
    """Check server setup without contacting Supabase or a model provider."""
    return {"status": "ok"}


@app.get("/api/students", response_model=list[StudentResponse], tags=["students"])
def list_students():
    """Expose the Phase 1 read query to the frontend."""
    try:
        return fetch_students(get_supabase_client())
    except Exception as exc:
        logging.getLogger(__name__).exception("Student lookup failed")
        raise HTTPException(
            503, "Unable to load students. Check the backend database settings."
        ) from exc


async def run_agent_request(question: str | None = None, chat_request: ChatRequest | None = None):
    """Let the agent retrieve records through its tool and return the answer."""
    try:
        agent = create_agent(chat=True) if chat_request is not None else create_agent()
    except AgentConfigurationError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        logging.getLogger(__name__).exception("Agent configuration failed")
        raise HTTPException(503, "Check GEMINI_MODEL and the provider configuration.") from exc

    try:
        if chat_request is not None:
            return await answer_chat(chat_request, agent)
        if question is None:
            return await answer_prad_question(agent)
        return await answer_question(question, agent)
    except StudentLookupError as exc:
        logging.getLogger(__name__).exception("Student lookup tool failed")
        raise HTTPException(503, "Unable to load student records from Supabase.") from exc
    except TimeoutError as exc:
        raise HTTPException(504, "The model took too long. Please try again.") from exc
    except Exception as exc:
        logging.getLogger(__name__).exception("Agent request failed")
        raise HTTPException(
            502, "The model request failed. Check the provider key and model."
        ) from exc


@app.post(
    "/api/agent/ask",
    response_model=AgentAnswer,
    tags=["agent"],
    summary="Ask the student database agent a question",
    responses={
        502: {"description": "Model provider or agent failure"},
        503: {"description": "Configuration or database lookup failure"},
        504: {"description": "Agent run exceeded its deadline"},
    },
)
async def ask_agent(request: AgentQuestion) -> AgentAnswer:
    """Accept JSON, await the tool-using agent, and return its answer and lookup metadata."""
    return await run_agent_request(request.question)


@app.post("/api/agent/prad", response_model=PradAnswer, tags=["agent"])
async def ask_about_prad():
    """Backward-compatible fixed question used by the existing frontend."""
    return await run_agent_request()


@app.post("/api/chat", response_model=AgentAnswer, tags=["chat"])
async def chat(request: ChatRequest) -> AgentAnswer:
    """Answer with the current tab's supplied history; no shared conversation state."""
    return await run_agent_request(chat_request=request)
