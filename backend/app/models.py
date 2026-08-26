from typing import Any, Literal

from pydantic import BaseModel, Field


AssistantStage = Literal["basic", "instructions", "all_context", "rag", "better_retrieval", "final"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str = Field(default="default", max_length=100)
    stage: AssistantStage | None = None


class Source(BaseModel):
    document: str
    section: str = ""
    score: float | None = None
    year: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []
    stage: str
    used_tool: str | None = None


class RetrievalResult(BaseModel):
    source: str
    section: str
    score: float
    text: str
    metadata: dict[str, Any]
