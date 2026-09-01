from pathlib import Path

from fastapi.testclient import TestClient

# Ensure KB path resolves before app import side effects in lifespan
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ["AGENTOPS_KB_PATH"] = str(ROOT / "data" / "sample_kb")

from app.main import app  # noqa: E402


def test_health_and_ask():
    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        ready = client.get("/readyz")
        assert ready.status_code == 200
        r = client.post("/v1/ask", json={"question": "Does AgentOps need AWS?"})
        assert r.status_code == 200
        body = r.json()
        assert "answer" in body
        assert isinstance(body["citations"], list)
        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "agentops_requests_total" in metrics.text
