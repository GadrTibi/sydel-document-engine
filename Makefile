.PHONY: install lint test run-ui

install:
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

lint:
	ruff check .
	mypy src

test:
	pytest

run-ui:
	streamlit run src/sydel_doc_engine/front_app/app.py
