.PHONY: install test eval ingest run bootstrap compose kind

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && PYTHONPATH=services/api pytest -q

eval:
	. .venv/bin/activate && PYTHONPATH=services/api python eval/run_eval.py

ingest:
	. .venv/bin/activate && PYTHONPATH=services/api python services/ingest/ingest.py

run:
	. .venv/bin/activate && AGENTOPS_KB_PATH=$$PWD/data/sample_kb PYTHONPATH=services/api uvicorn app.main:app --host 127.0.0.1 --port 8080

bootstrap:
	./scripts/bootstrap_local.sh

compose:
	docker compose up --build api prometheus

kind:
	./scripts/kind_up.sh
