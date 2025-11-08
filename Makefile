.PHONY: dev lint format type-check test

dev:
	uv run uvicorn app.main:app --reload

lint:
	uvx ruff check .

format:
	uvx ruff format .

type-check:
	uvx pyright

test:
	uv run pytest

check: format lint type-check

