# Incident Response — Elevated Error Rate

## Severity
- SEV-1: >5% 5xx for 5 minutes on `/v1/ask`
- SEV-2: latency p95 > 2s sustained

## First 15 minutes
1. Check Grafana (or compose Prometheus) for request rate and error ratio.
2. Confirm agent readiness: `GET /readyz` must be 200.
3. Look at recent deploys; if a release landed in the last hour, prepare rollback.
4. Search KB for similar past incidents before changing config.

## Mitigation playbook
- Rate limit tightening: lower `AGENTOPS_RATE_LIMIT_PER_MIN` and restart.
- Disable optional tools if a mock dependency flaps: set `AGENTOPS_TOOLS_ENABLED=search_kb` only.
- Scale API replicas in the overlay (dev uses 1; bump replicas in kustomization).

## Post-incident
- Capture timeline, add a golden eval case if the agent gave a wrong answer.
- File follow-up for missing runbook coverage.
