"""Student and fixed-question agent endpoints for the workshop preview."""
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from backend import config  # noqa: F401 -- loads backend/.env
from backend.agent import QUESTION, AgentConfigurationError, answer_prad_question, create_agent
from backend.db_client import get_supabase_client
from backend.exercise import fetch_students
from backend.schemas import PradAnswer, StudentResponse

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


@app.post("/api/agent/prad", response_model=PradAnswer, tags=["agent"])
async def ask_about_prad():
    """Fetch fresh records, inject them into the prompt, and return the agent's answer."""
    try:
        agent = create_agent()
    except AgentConfigurationError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        logging.getLogger(__name__).exception("Agent configuration failed")
        raise HTTPException(503, "Check GEMINI_MODEL and the provider configuration.") from exc

    try:
        records = await run_in_threadpool(lambda: fetch_students(get_supabase_client()))
    except Exception as exc:
        logging.getLogger(__name__).exception("Student lookup for agent failed")
        raise HTTPException(503, "Unable to load student records from Supabase.") from exc

    try:
        answer = await answer_prad_question(records, agent)
    except TimeoutError as exc:
        raise HTTPException(504, "The model took too long. Please try again.") from exc
    except Exception as exc:
        logging.getLogger(__name__).exception("Agent request failed")
        raise HTTPException(
            502, "The model request failed. Check the provider key and model."
        ) from exc

    return PradAnswer(question=QUESTION, answer=answer, records_analyzed=len(records))


# Phase 4 can generalize this fixed-question preview into a question-taking endpoint.
# TODO (Phase 6): Extend the contract to support separate conversations.
