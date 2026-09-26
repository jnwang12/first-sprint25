"""Phase 4 HTTP contract checks; all model calls are replaced locally."""

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from backend import main
from backend.schemas import AgentAnswer


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"question": ""},
        {"question": "   "},
        {"question": "x" * 501},
        {"question": 123},
        {"question": "Prad?", "extra": True},
    ],
)
def test_invalid_questions_do_not_invoke_provider(monkeypatch, body):
    create = Mock(side_effect=AssertionError("Invalid input must not invoke the provider"))
    monkeypatch.setattr(main, "create_agent", create)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/ask", json=body)
    assert response.status_code == 422
    create.assert_not_called()


def test_question_is_forwarded_and_response_serialized(monkeypatch):
    agent = object()
    monkeypatch.setattr(main, "create_agent", lambda: agent)
    result = AgentAnswer(
        question="How many records have a name of Prad?",
        answer="There are 3.",
        records_analyzed=6,
        tool_calls=1,
    )
    answer = AsyncMock(return_value=result)
    monkeypatch.setattr(main, "answer_question", answer)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/ask", json={"question": f"  {result.question}  "})
    assert response.status_code == 200
    assert response.json() == result.model_dump()
    answer.assert_awaited_once_with(result.question, agent)


@pytest.mark.parametrize("failure,status", [(TimeoutError(), 504), (RuntimeError("secret"), 502)])
def test_api_provider_errors(monkeypatch, failure, status):
    monkeypatch.setattr(main, "create_agent", lambda: object())
    monkeypatch.setattr(main, "answer_question", AsyncMock(side_effect=failure))
    with TestClient(main.app) as client:
        response = client.post("/api/agent/ask", json={"question": "How many Prad records?"})
    assert response.status_code == status
    assert "secret" not in response.text
