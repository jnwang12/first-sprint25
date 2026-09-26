"""Server scaffolding. The agent endpoint is a Phase 4 exercise."""
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend import config  # noqa: F401 -- loads backend/.env
from backend.db_client import get_supabase_client
from backend.exercise import fetch_students
from backend.schemas import StudentResponse

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


# TODO (Phase 4): Define an endpoint that invokes your agent and returns its answer.
# TODO (Phase 4): Define the request/response contract in schemas.py.
# TODO (Phase 6): Extend the contract to support separate conversations.
