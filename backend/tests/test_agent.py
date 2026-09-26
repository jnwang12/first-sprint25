"""Exercise tool execution with a local model and no network or paid provider."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient
from pydantic_ai import models
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models.function import FunctionModel

from backend import main
from backend.agent import QUESTION, answer_prad_question, create_agent
from backend.schemas import PradAnswer
from backend.tools import StudentLookupError


@pytest.fixture(autouse=True)
def disable_model_network(monkeypatch):
    monkeypatch.setattr(models, "ALLOW_MODEL_REQUESTS", False)


@pytest.mark.parametrize("names", [["prad", "Prad", " PRAD ", "Pradeep"], []])
@pytest.mark.parametrize("skip_first_lookup", [False, True])
def test_agent_calls_tool_before_answering(names, skip_first_lookup):
    records = [{"name": name, "email": "private@example.com", "major": "Math"} for name in names]
    loader = Mock(return_value=records)
    steps = 0

    def local_model(messages, info):
        nonlocal steps
        steps += 1
        assert [tool.name for tool in info.function_tools] == ["get_student_names"]
        assert "ignoring capitalization" in info.instructions
        prompts = [
            part.content
            for message in messages
            for part in message.parts
            if isinstance(part, UserPromptPart)
        ]
        assert prompts == [QUESTION]  # No database rows are injected into the initial prompt.
        tool_results = [
            part
            for message in messages
            for part in message.parts
            if isinstance(part, ToolReturnPart)
        ]
        if not tool_results:
            loader.assert_not_called()
            if skip_first_lookup and steps == 1:
                return ModelResponse(parts=[TextPart("An unsupported guess.")])
            return ModelResponse(parts=[ToolCallPart("get_student_names", {}, "lookup-1")])
        assert tool_results[-1].content == [{"name": name} for name in names]
        assert "private@example.com" not in str(tool_results[-1].content)
        loader.assert_called_once()
        return ModelResponse(parts=[TextPart("Answer based on the tool result.")])

    agent = create_agent(FunctionModel(local_model))
    response = asyncio.run(answer_prad_question(agent, load_students=loader))
    assert response.answer == "Answer based on the tool result."
    assert response.tool_calls == 1
    assert response.records_analyzed == len(records)
    assert steps == (3 if skip_first_lookup else 2)


def test_refuses_answer_without_tool():
    def local_model(messages, info):
        return ModelResponse(parts=[TextPart("An unsupported guess.")])

    loader = Mock()
    with pytest.raises(UnexpectedModelBehavior):
        asyncio.run(
            answer_prad_question(create_agent(FunctionModel(local_model)), load_students=loader)
        )
    loader.assert_not_called()


def test_tool_failure_is_not_an_empty_result():
    def local_model(messages, info):
        return ModelResponse(parts=[ToolCallPart("get_student_names", {}, "lookup-1")])

    with pytest.raises(StudentLookupError):
        asyncio.run(
            answer_prad_question(
                create_agent(FunctionModel(local_model)),
                load_students=Mock(side_effect=RuntimeError("private database detail")),
            )
        )


def test_missing_key_returns_actionable_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_endpoint_delegates_to_agent_without_prefetch(monkeypatch):
    agent = object()
    monkeypatch.setattr(main, "create_agent", lambda: agent)
    lookup = Mock(side_effect=AssertionError("The endpoint must not pre-fetch records"))
    monkeypatch.setattr(main, "fetch_students", lookup)
    result = PradAnswer(
        question=QUESTION,
        answer="There is 1 matching record.",
        records_analyzed=1,
        tool_calls=1,
    )
    answer = AsyncMock(return_value=result)
    monkeypatch.setattr(main, "answer_prad_question", answer)
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == 200
    assert response.json() == result.model_dump()
    answer.assert_awaited_once_with(agent)
    lookup.assert_not_called()


@pytest.mark.parametrize(
    "failure,status",
    [
        (TimeoutError(), 504),
        (RuntimeError("secret"), 502),
        (StudentLookupError("secret"), 503),
    ],
)
def test_failures_are_safe(monkeypatch, failure, status):
    monkeypatch.setattr(main, "create_agent", lambda: object())
    monkeypatch.setattr(main, "answer_prad_question", AsyncMock(side_effect=failure))
    with TestClient(main.app) as client:
        response = client.post("/api/agent/prad")
    assert response.status_code == status
    assert "secret" not in response.text


@pytest.mark.parametrize("key_variable", ["GEMINI_API_KEY", "GOOGLE_API_KEY"])
def test_gemini_key_configuration(monkeypatch, key_variable):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv(key_variable, "test-key-not-real")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    configured = create_agent()
    assert configured.model.model_name == "gemini-3.1-flash-lite"
