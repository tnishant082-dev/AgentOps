from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from .rag import Hit, KnowledgeIndex


@dataclass
class ToolResult:
    name: str
    ok: bool
    detail: str
    data: dict | None = None


# Mock service registry — stands in for real mesh / LB health without cloud cost.
_MOCK_SERVICES = {
    "agentops-api": {"status": "healthy", "replicas": 1, "p95_ms": 42},
    "ingest": {"status": "healthy", "replicas": 1, "p95_ms": 18},
    "prometheus": {"status": "healthy", "replicas": 1, "p95_ms": 11},
}


def search_kb(index: KnowledgeIndex, query: str, top_k: int = 3) -> ToolResult:
    hits = index.search(query, top_k=top_k)
    summary = ", ".join(f"{h.chunk.path} ({h.score:.2f})" for h in hits) or "no hits"
    return ToolResult(
        name="search_kb",
        ok=True,
        detail=f"retrieved {len(hits)} chunks: {summary}",
        data={"hits": hits},
    )


def get_service_status(service: str | None = None) -> ToolResult:
    if service:
        info = _MOCK_SERVICES.get(service)
        if not info:
            return ToolResult(
                name="get_service_status",
                ok=False,
                detail=f"unknown service '{service}'",
                data={"known": list(_MOCK_SERVICES)},
            )
        return ToolResult(
            name="get_service_status",
            ok=info["status"] == "healthy",
            detail=f"{service}: {info['status']} replicas={info['replicas']} p95={info['p95_ms']}ms",
            data={service: info},
        )
    return ToolResult(
        name="get_service_status",
        ok=all(v["status"] == "healthy" for v in _MOCK_SERVICES.values()),
        detail="fleet snapshot",
        data=dict(_MOCK_SERVICES),
    )


def pick_tools(question: str, enabled: set[str]) -> list[str]:
    """Tiny router — production agents often use LLM tool choice; we keep it local."""
    q = question.lower()
    chosen: list[str] = []
    if "search_kb" in enabled:
        chosen.append("search_kb")
    if "get_service_status" in enabled and any(
        k in q for k in ("status", "health", "down", "latency", "error rate", "replica")
    ):
        chosen.append("get_service_status")
    return chosen or (["search_kb"] if "search_kb" in enabled else [])


TOOL_FN: dict[str, Callable] = {
    "search_kb": search_kb,
    "get_service_status": get_service_status,
}


def now_ms() -> int:
    return int(time.time() * 1000)
