"""Shared Supabase connection setup; querying the table is left to the exercises."""
import os
from functools import lru_cache

from supabase import Client, create_client

from backend import config  # noqa: F401 -- loads backend/.env


@lru_cache
def get_supabase_client() -> Client:
    """Initialize once, on first use; the starter boots without cloud credentials."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Set SUPABASE_URL and SUPABASE_KEY in backend/.env before this exercise."
        )
    return create_client(url, key)

