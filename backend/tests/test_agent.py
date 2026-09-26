"""Exercise the real Pydantic AI pipeline with a local model, never a paid provider."""
import asyncio
import json
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic_ai import Agent, models
from pydantic_ai.messages import ModelResponse, TextPart, UserPromptPart
from pydantic_ai.models.function import FunctionModel

from backend import main
from backend.agent import INSTRUCTIONS, QUESTION, answer_prad_question


@pytest.fixture(autouse=True)
def disable_model_network(monkeypatch):
    monkeypatch.setattr(models, "ALLOW_MODEL_REQUESTS", False)


@pytest.mark.parametrize("names", [["prad", "Prad", " PRAD ", "Pradeep"], []])
def test_prompt_contains_rows_and_no_tools(names):
    records = [{"name": name, "email": "private@example.com", "major": "Math"} for name in names]

    def local_model(messages, info):
        assert info.function_tools == []
        assert info.output_tools == []
        assert "ignoring capitalization" in info.instructions
        prompts = [
            part.content for message in messages for part in message.parts
            if isinstance(part, UserPromptPart)
        ]
        prompt = prompts[-1]
        assert QUESTION in prompt
        assert "private@example.com" not in prompt
        assert json.loads(prompt.split("Student records (JSON):\n")[1]) == [
            {"name": name} for name in names
        ]
        return ModelResponse(parts=[TextPart("Local test-model answer.")])

    agent = Agent(FunctionModel(local_model), instructions=INSTRUCTIONS, output_type=str)
    assert asyncio.run(answer_prad_question(records, agent)) == "Local test-model answer."


def test_missing_key_returns_actionable_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_endpoint_uses_fresh_records_and_agent_answer(monkeypatch):
    records = [{"name": "prad", "email": "test@example.com", "major": "Math"}]
    agent = object()
    monkeypatch.setattr(main, "create_agent", lambda: agent)
    monkeypatch.setattr(main, "get_supabase_client", lambda: object())
    monkeypatch.setattr(main, "fetch_students", lambda client: records)
    answer = AsyncMock(return_value="There is 1 matching record.")
    monkeypatch.setattr(main, "answer_prad_question", answer)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == 200
    assert response.json() == {
        "question": QUESTION, "answer": "There is 1 matching record.", "records_analyzed": 1,
    }
    answer.assert_awaited_once_with(records, agent)


@pytest.mark.parametrize("failure,status", [(TimeoutError(), 504), (RuntimeError("secret"), 502)])
def test_provider_failures_are_safe(monkeypatch, failure, status):
    monkeypatch.setattr(main, "create_agent", lambda: object())
    monkeypatch.setattr(main, "get_supabase_client", lambda: object())
    monkeypatch.setattr(main, "fetch_students", lambda client: [])
    monkeypatch.setattr(main, "answer_prad_question", AsyncMock(side_effect=failure))
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == status
    assert "secret" not in response.text
