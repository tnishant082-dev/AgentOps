# Kubernetes Ops Notes (kind)

## Cluster
We use kind (Kubernetes in Docker). No managed control plane bill.

```bash
kind create cluster --name agentops --config infra/terraform/kind-config.yaml
kubectl apply -k k8s/overlays/dev
```

## Health probes
- liveness: `/healthz` — process up
- readiness: `/readyz` — vector index loaded and tools reachable

## GitOps-style apply
CI builds the image, then (on main, optional) applies the overlay. Without a remote cluster, the workflow validates manifests with `kubectl kustomize`.

## Config via Kustomize
- `k8s/base` — Deployment, Service, ConfigMap, ServiceAccount
- `overlays/dev` — 1 replica, local image, lower rate limit
- `overlays/prod` — 2 replicas, stricter limits (still local/kind)

## Observability
Prometheus scrapes `/metrics` on the API. Grafana dashboards (compose) show QPS and error rate.
