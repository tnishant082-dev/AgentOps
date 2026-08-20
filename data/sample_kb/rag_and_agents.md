# RAG & Agent Design (AgentOps)

## Retrieval
Default backend is TF-IDF + cosine similarity over the markdown KB under `data/sample_kb`. No paid embedding API. Optional swap to sentence-transformers or an OpenAI-compatible endpoint later — the `LLMBackend` interface stays the same.

## Agent loop
1. Parse user question
2. Decide tools: always `search_kb`; optionally `get_service_status`
3. Gather citations + status
4. Compose answer with the local stub LLM (deterministic template over retrieved chunks)

## Production concerns covered
- Rate limiting per client IP
- Health / readiness probes for k8s
- Eval harness with golden questions (must cite sources)
- Structured JSON responses with `citations[]` and `tools_used[]`

## Cost posture
Everything runs offline. Zero AWS/GCP spend. No required LLM API keys.
