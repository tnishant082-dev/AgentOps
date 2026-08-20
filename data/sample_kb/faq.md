# AgentOps FAQ

**Q: Does this project need AWS?**
A: No. Terraform here only targets kind / docker-local resources. Cloud providers are intentionally omitted to keep the bill at zero.

**Q: How do I roll back a bad deploy?**
A: `kubectl -n agentops rollout undo deploy/agentops-api`, then confirm `/healthz`.

**Q: What if the agent invents an answer?**
A: Prefer citations. The eval suite fails if required source docs are missing from `citations`. Add golden cases under `eval/`.

**Q: Can I plug in a real LLM later?**
A: Yes. Implement `LLMBackend` in `services/api/app/llm.py`. Default remains `local_stub`.

**Q: How do I run everything locally?**
A: `./scripts/bootstrap_local.sh` (compose path) or follow the kind section in the README.
