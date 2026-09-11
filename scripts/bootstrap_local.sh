#!/usr/bin/env bash
# One-command local bring-up where possible.
# Prefer compose; document kind for reviewers with Docker Desktop / kind installed.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> AgentOps bootstrap (local-first, \$0 cloud)"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

echo "==> Ingest KB"
python services/ingest/ingest.py

echo "==> Run unit tests + eval"
pytest -q
python eval/run_eval.py

echo "==> Starting API on :8080 (Ctrl+C to stop)"
export AGENTOPS_KB_PATH="$ROOT/data/sample_kb"
export PYTHONPATH="$ROOT/services/api${PYTHONPATH:+:$PYTHONPATH}"
exec uvicorn app.main:app --host 127.0.0.1 --port 8080
