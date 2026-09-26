"""Convert a bounded text transcript to Pydantic AI history, without server storage."""

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart

from backend.agent import answer_question
from backend.schemas import AgentAnswer, ChatRequest


async def answer_chat(request: ChatRequest, agent: Agent, *, load_students=None) -> AgentAnswer:
    history: list[ModelMessage] = []
    for message in request.history:
        if message.role == "user":
            history.append(ModelRequest(parts=[UserPromptPart(message.content)]))
        else:
            history.append(ModelResponse(parts=[TextPart(message.content)]))
    return await answer_question(
        request.question,
        agent,
        load_students=load_students,
        message_history=history,
    )
