from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from .agent import OpsAgent
from .config import settings
from .llm import get_llm
from .metrics import metrics
from .rag import KnowledgeIndex
from .ratelimit import SlidingWindowLimiter

index = KnowledgeIndex()
limiter = SlidingWindowLimiter(settings.rate_limit_per_min)
agent: OpsAgent | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global agent
    n = index.load(settings.kb_path)
    metrics.set("agentops_index_chunks", float(n))
    agent = OpsAgent(index, get_llm(settings.llm_backend), settings.enabled_tools)
    yield


app = FastAPI(
    title="AgentOps",
    description="Local-first ops knowledge agent — zero cloud bill by design.",
    version="0.1.0",
    lifespan=lifespan,
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    citations: list[dict]
    tools_used: list[str]
    tool_notes: list[str]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    if not index.ready or agent is None:
        raise HTTPException(status_code=503, detail="index not ready")
    return {"status": "ready", "chunks": len(index.chunks)}


@app.get("/metrics")
def prometheus_metrics():
    return PlainTextResponse(metrics.render(), media_type="text/plain; version=0.0.4")


@app.post("/v1/ask", response_model=AskResponse)
def ask(body: AskRequest, request: Request):
    if agent is None:
        raise HTTPException(status_code=503, detail="agent not ready")
    client = request.client.host if request.client else "unknown"
    if not limiter.allow(client):
        metrics.inc("agentops_requests_total", status="429")
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    try:
        result = agent.ask(body.question)
        metrics.inc("agentops_requests_total", status="200")
        return AskResponse(
            answer=result.answer,
            citations=result.citations,
            tools_used=result.tools_used,
            tool_notes=result.tool_notes,
        )
    except Exception as exc:  # noqa: BLE001 — surface as 500 for ops demos
        metrics.inc("agentops_requests_total", status="500")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/v1/services")
def list_services():
    from .tools import get_service_status

    result = get_service_status()
    return result.data
