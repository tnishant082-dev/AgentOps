from __future__ import annotations

from dataclasses import dataclass, field

from .llm import LLMBackend
from .rag import Hit, KnowledgeIndex
from .tools import get_service_status, pick_tools, search_kb


@dataclass
class AgentResponse:
    answer: str
    citations: list[dict]
    tools_used: list[str] = field(default_factory=list)
    tool_notes: list[str] = field(default_factory=list)


class OpsAgent:
    def __init__(self, index: KnowledgeIndex, llm: LLMBackend, enabled_tools: set[str]):
        self.index = index
        self.llm = llm
        self.enabled_tools = enabled_tools

    def ask(self, question: str) -> AgentResponse:
        tools = pick_tools(question, self.enabled_tools)
        hits: list[Hit] = []
        notes: list[str] = []
        used: list[str] = []

        for name in tools:
            if name == "search_kb":
                result = search_kb(self.index, question, top_k=3)
                used.append(name)
                notes.append(result.detail)
                if result.data and "hits" in result.data:
                    hits = result.data["hits"]
            elif name == "get_service_status":
                result = get_service_status()
                used.append(name)
                notes.append(result.detail)

        draft = self.llm.compose(question, hits, notes)
        return AgentResponse(
            answer=draft.text,
            citations=draft.citations,
            tools_used=used,
            tool_notes=notes,
        )
