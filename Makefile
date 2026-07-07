install:
	uv sync

build:
	uv run ruff check --fix
	uv run ruff format
	uv build

package-install: build
	uv tool install --force $(wildcard dist/*.whl)

lint:
	uv run ruff check --fix

format:
	uv run ruff format

test:
	uv run pytest --cov=gendiff --cov-report=term --cov-report=xml

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml

test-build:	build package-install

start:
	docker run --rm -d -p 5173:5173 --name kanban_board hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

stop:
	docker stop kanban_board