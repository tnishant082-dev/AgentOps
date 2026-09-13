# Architecture — Cloud AI Engineer stairs → this repo

AgentOps is a single repo that walks the full staircase without a cloud bill.

## Layer map

| Stair | What you practice | Where in the repo | How to demo |
|---|---|---|---|
| 1. Linux / Networking / Cloud concepts | Bridge networks as VPC stand-in, private vs published services, DNS between containers | `docker-compose.yml`, `data/sample_kb/networking_basics.md`, `docs/architecture.md` | `docker compose up api prometheus` and inspect `agentops-net` |
| 2. Docker, Terraform, CI/CD | Multi-stage-ish slim image, compose topology, Terraform for kind/local only, Actions | `services/api/Dockerfile`, `infra/terraform/`, `.github/workflows/ci.yml` | `terraform plan`; push triggers CI |
| 3. Kubernetes + observability + GitOps-style | kind manifests, probes, Kustomize overlays, Prometheus scrape | `k8s/`, `observability/`, `scripts/kind_up.sh` | `kubectl apply -k k8s/overlays/dev` |
| 4. LLM APIs + RAG + vectors | Abstracted `LLMBackend`, default local stub, TF-IDF retrieval (sklearn) | `services/api/app/{llm,rag}.py`, `services/ingest/`, `data/sample_kb/` | `python services/ingest/ingest.py` then ask via API |
| 5. Agent in production | FastAPI, tool loop, rate limit, health/ready, metrics, eval, docker→kind | `services/api/app/`, `eval/`, `tests/` | `./scripts/bootstrap_local.sh` |

## Request path

```
Client
  → FastAPI (/v1/ask)
    → rate limiter
      → OpsAgent
        → tools: search_kb (TF-IDF) [+ get_service_status mock]
        → LocalStubLLM composes answer + citations
      → Prometheus counters on /metrics
```

## Cost boundary

Nothing in this repository provisions AWS/GCP/Azure resources. Terraform providers are `local` + `null`. The LLM default is offline. Optional paid APIs are extension points only and are not wired in CI.

## Why TF-IDF instead of a hosted vector DB

Portfolio demos fail when reviewers hit missing API keys. sklearn TF-IDF is deterministic, dependency-light, and good enough for a small ops runbook corpus. The `KnowledgeIndex` interface can later wrap Chroma/FAISS/OpenAI embeddings without changing the agent loop.
