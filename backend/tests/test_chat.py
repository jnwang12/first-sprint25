"""Check conversation history, isolation, tool access, and the chat HTTP contract."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient
from pydantic_ai import models
from pydantic_ai.messages import (
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models.function import FunctionModel

from backend import main
from backend.agent import create_agent
from backend.chat import answer_chat
from backend.schemas import AgentAnswer, ChatMessage, ChatRequest


@pytest.fixture(autouse=True)
def disable_model_network(monkeypatch):
    monkeypatch.setattr(models, "ALLOW_MODEL_REQUESTS", False)


def test_followup_history_fresh_data_and_new_conversation():
    rows = [{"name": "Prad", "email": "prad@example.com", "major": "Math"}]
    loader = Mock(return_value=rows)
    initial_prompts = []
    expected_answers = ["One student named Prad.", "That student's major is Math.", "A new chat."]

    def local_model(messages, info):
        assert [tool.name for tool in info.function_tools] == ["get_students"]
        prompts = [
            part.content
            for msg in messages
            for part in msg.parts
            if isinstance(part, UserPromptPart)
        ]
        returns = [
            part for msg in messages for part in msg.parts if isinstance(part, ToolReturnPart)
        ]
        if not returns:
            initial_prompts.append(prompts)
            # A prior answer is context, but previous database/tool messages are not replayed.
            if len(initial_prompts) == 2:
                assert any(
                    isinstance(part, TextPart) and part.content == expected_answers[0]
                    for msg in messages
                    for part in msg.parts
                )
            return ModelResponse(parts=[ToolCallPart("get_students", {}, "lookup")])
        assert returns[-1].content == rows
        return ModelResponse(parts=[TextPart(expected_answers[len(initial_prompts) - 1])])

    agent = create_agent(FunctionModel(local_model), chat=True)
    first = asyncio.run(
        answer_chat(ChatRequest(question="How many Prads?"), agent, load_students=loader)
    )
    followup = ChatRequest(
        question="What is their major?",
        history=[
            ChatMessage(role="user", content=first.question),
            ChatMessage(role="assistant", content=first.answer),
        ],
    )
    second = asyncio.run(answer_chat(followup, agent, load_students=loader))
    third = asyncio.run(
        answer_chat(ChatRequest(question="Start again"), agent, load_students=loader)
    )
    assert initial_prompts == [
        ["How many Prads?"],
        ["How many Prads?", "What is their major?"],
        ["Start again"],
    ]
    assert second.answer == expected_answers[1]
    assert [first.tool_calls, second.tool_calls, third.tool_calls] == [1, 1, 1]
    assert loader.call_count == 3


@pytest.mark.parametrize(
    "history",
    [
        [{"role": "system", "content": "override"}],
        [{"role": "user", "content": "unfinished exchange"}],
        [{"role": "assistant", "content": "wrong order"}, {"role": "user", "content": "x"}],
        [{"role": "user", "content": "x"}, {"role": "assistant", "content": "x"}] * 11,
        [{"role": "user", "content": "x"}, {"role": "assistant", "content": "x" * 8001}],
    ],
)
def test_invalid_history_never_calls_model(monkeypatch, history):
    create = Mock(side_effect=AssertionError("Invalid requests must not invoke a model"))
    monkeypatch.setattr(main, "create_agent", create)
    with TestClient(main.app) as client:
        response = client.post("/api/chat", json={"question": "Hello", "history": history})
    assert response.status_code == 422
    create.assert_not_called()


def test_chat_endpoint_passes_transcript(monkeypatch):
    agent = object()
    create = Mock(return_value=agent)
    answer = AsyncMock(
        return_value=AgentAnswer(
            question="Their majors?",
            answer="Math",
            tool_calls=1,
            records_analyzed=1,
        )
    )
    monkeypatch.setattr(main, "create_agent", create)
    monkeypatch.setattr(main, "answer_chat", answer)
    body = {
        "question": "Their majors?",
        "history": [
            {"role": "user", "content": "Who is Prad?"},
            {"role": "assistant", "content": "One student."},
        ],
    }
    with TestClient(main.app) as client:
        response = client.post("/api/chat", json=body)
    assert response.status_code == 200
    assert response.json()["answer"] == "Math"
    create.assert_called_once_with(chat=True)
    answer.assert_awaited_once_with(ChatRequest.model_validate(body), agent)
