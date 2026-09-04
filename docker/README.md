# Docker notes

- `docker compose up --build api prometheus` — API + metrics scrape path
- `docker compose --profile ui up grafana` — optional Grafana on :3000
- `docker compose --profile batch run --rm ingest` — rebuild KB manifest

Images stay on the local daemon / kind node. No paid registry required.
Public GHCR push is optional and free for public repos.
