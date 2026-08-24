from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .rag import Hit


@dataclass
class AnswerDraft:
    text: str
    citations: list[dict]


class LLMBackend(ABC):
    @abstractmethod
    def compose(self, question: str, hits: list[Hit], tool_notes: list[str]) -> AnswerDraft:
        raise NotImplementedError


class LocalStubLLM(LLMBackend):
    """Deterministic offline composer — no API keys, no network."""

    def compose(self, question: str, hits: list[Hit], tool_notes: list[str]) -> AnswerDraft:
        if not hits:
            body = (
                "I could not find matching runbooks in the local knowledge base. "
                "Try rephrasing or ingesting more docs under data/sample_kb/."
            )
            return AnswerDraft(text=body, citations=[])

        bullets: list[str] = []
        citations: list[dict] = []
        for h in hits:
            excerpt = _short(h.chunk.text, 280)
            bullets.append(f"- From **{h.chunk.title}** (`{h.chunk.path}`): {excerpt}")
            citations.append(
                {
                    "doc_id": h.chunk.doc_id,
                    "title": h.chunk.title,
                    "path": h.chunk.path,
                    "score": round(h.score, 4),
                }
            )

        notes = ""
        if tool_notes:
            notes = "\n\n**Live checks**\n" + "\n".join(f"- {n}" for n in tool_notes)

        text = (
            f"Based on the local ops KB for: _{question.strip()}_\n\n"
            + "\n".join(bullets)
            + notes
            + "\n\n_Answers are retrieval-grounded (TF-IDF). No external LLM was called._"
        )
        return AnswerDraft(text=text, citations=citations)


def get_llm(name: str) -> LLMBackend:
    if name in ("local_stub", "local", "stub"):
        return LocalStubLLM()
    # Extension point for OpenAI-compatible backends later — still optional.
    raise ValueError(f"unsupported LLM backend: {name}")


def _short(text: str, n: int) -> str:
    flat = " ".join(text.split())
    if len(flat) <= n:
        return flat
    return flat[: n - 1].rstrip() + "…"
