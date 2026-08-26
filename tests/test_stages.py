import pytest
from pydantic import ValidationError

from app.assistant.orchestrator import AssistantOrchestrator
from app.config import Settings
from app.models import ChatRequest


class RecordingProvider:
    async def complete(self, system: str, message: str) -> str:
        return f"response for {message}"


class StubRetriever:
    async def search(self, message: str, filters=None):
        return [
            {
                "source": "test.md",
                "section": "Test",
                "score": 0.9,
                "text": f"Evidence for {message}",
                "year": 2026,
            }
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "stage",
    ["basic", "instructions", "all_context", "rag", "better_retrieval", "final"],
)
async def test_requested_stage_overrides_configured_default(stage, tmp_path):
    settings = Settings(_env_file=None, assistant_stage="basic", knowledge_path=tmp_path)
    orchestrator = AssistantOrchestrator(settings, RecordingProvider(), StubRetriever())

    result = await orchestrator.chat("test question", "conversation", stage)

    assert result["stage"] == stage


def test_chat_request_rejects_unknown_stage():
    with pytest.raises(ValidationError):
        ChatRequest(message="test", stage="unknown")

