# Deploy Runbook — AgentOps API

## Preconditions
- Image built and tagged `agentops-api:local`
- kind cluster running (`kind create cluster --name agentops`)
- Overlay applied: `kubectl apply -k k8s/overlays/dev`

## Steps
1. Confirm pods: `kubectl -n agentops get pods`
2. Wait for readiness: `kubectl -n agentops rollout status deploy/agentops-api`
3. Smoke health: `curl http://localhost:8080/healthz` (via port-forward)
4. Ask a sample question: `curl -s -X POST http://localhost:8080/v1/ask -H 'content-type: application/json' -d '{"question":"How do I roll back a bad deploy?"}'`

## Rollback
- `kubectl -n agentops rollout undo deploy/agentops-api`
- Verify previous ReplicaSet is active and `/healthz` returns 200.

## Common failures
- CrashLoopBackOff: check `AGENTOPS_KB_PATH` mount and logs.
- ImagePullBackOff: for kind, load the image with `kind load docker-image agentops-api:local --name agentops`.
