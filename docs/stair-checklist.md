# Stair checklist (reviewer cheat sheet)

- [ ] Layer 1: Read `networking_basics.md`; note compose network `agentops-net`
- [ ] Layer 2: Open `infra/terraform/main.tf` — confirm no AWS provider; skim `ci.yml`
- [ ] Layer 3: `kustomize build k8s/overlays/dev` (or CI job); probes on Deployment
- [ ] Layer 4: Run ingest + ask a FAQ question; citations present
- [ ] Layer 5: `pytest` + `eval/run_eval.py` green; `/healthz` + `/readyz` + `/metrics`
