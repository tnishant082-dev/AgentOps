# Linux Networking & Local Cloud Topology

AgentOps uses a docker-compose network named `agentops-net` to stand in for a VPC.

## Concepts mapped to local
| Cloud idea | Local stand-in |
|---|---|
| VPC / subnet | bridge network `agentops-net` |
| Security group | compose `expose` / published ports only on API |
| Load balancer | compose service name DNS + optional nginx |
| Private service | ingest + prometheus with no host ports |
| Bastion | `scripts/bootstrap_local.sh` port-forwards |

## Useful checks
- `ip addr` / `ss -tlnp` on the API container
- DNS between services: from api, `getent hosts prometheus`
- Latency between peers: `ping -c 3 ingest` (if ping present)

## Why this matters for agents
Tools like `get_service_status` mock network-reachable health endpoints. In real cloud you would hit ALB/NLB targets; here we hit compose DNS names so the agent loop stays honest about dependency health without paying for cloud networking.
