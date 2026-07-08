install:
	uv sync

lint:
	uv run ruff check --fix

format:
	uv run ruff format

start:
	docker run --rm -d -p 5173:5173 --name kanban_board hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

stop:
	docker stop kanban_board

test: start
	uv run pytest -k smoke --alluredir=reports
	docker stop kanban_board