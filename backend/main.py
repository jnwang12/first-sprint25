"""Server scaffolding. The agent endpoint is a Phase 4 exercise."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import config  # noqa: F401 -- loads backend/.env

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


# TODO (Phase 4): Define an endpoint that invokes your agent and returns its answer.
# TODO (Phase 4): Define the request/response contract in schemas.py.
# TODO (Phase 6): Extend the contract to support separate conversations.
