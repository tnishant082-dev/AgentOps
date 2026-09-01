from pathlib import Path

from app.agent import OpsAgent
from app.llm import get_llm
from app.rag import KnowledgeIndex

ROOT = Path(__file__).resolve().parents[1]


def _agent() -> OpsAgent:
    idx = KnowledgeIndex()
    idx.load(ROOT / "data" / "sample_kb")
    return OpsAgent(idx, get_llm("local_stub"), {"search_kb", "get_service_status"})


def test_ask_returns_citations():
    res = _agent().ask("How do I roll back a bad deploy?")
    assert res.citations
    assert "search_kb" in res.tools_used
    assert "rollout undo" in res.answer.lower() or "rollback" in res.answer.lower()


def test_status_uses_tool():
    res = _agent().ask("What is the health status of the fleet?")
    assert "get_service_status" in res.tools_used
