#!/usr/bin/env bash
# Optional path for reviewers with Docker + kind.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

command -v docker >/dev/null || { echo "docker required"; exit 1; }
command -v kind >/dev/null || { echo "kind required — https://kind.sigs.k8s.io/"; exit 1; }
command -v kubectl >/dev/null || { echo "kubectl required"; exit 1; }

docker build -t agentops-api:local -f services/api/Dockerfile .
kind create cluster --name agentops --config infra/terraform/kind-config.yaml || true
kind load docker-image agentops-api:local --name agentops
kubectl apply -k k8s/overlays/dev
kubectl -n agentops rollout status deploy/agentops-api --timeout=120s
echo "Port-forward: kubectl -n agentops port-forward svc/agentops-api 8080:80"
