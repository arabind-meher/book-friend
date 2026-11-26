.PHONY: install run worker migrate lint format test check services up down logs

install:
	uv sync

run:
	uv run python manage.py runserver

worker:
	uv run python manage.py rqworker default

migrate:
	uv run python manage.py migrate

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
	uv run ruff format .

test:
	uv run pytest

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest

services:
	docker compose up -d postgres redis

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f
