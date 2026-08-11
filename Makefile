.PHONY: install init run test lint demo
install:
	pip install -e '.[dev]'
init:
	python scripts/init_db.py
run:
	uvicorn app.main:app --reload
test:
	pytest
lint:
	ruff check .
demo:
	python scripts/demo_run.py
