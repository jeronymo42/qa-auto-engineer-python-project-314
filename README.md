# Тестирование канбан-доски с Selenium (Python)

## Запуск тестирумоего приложения локально
Выполнить команду:
```
make start
```
или 

```
docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app
```
## Запуск тестов
(Контейнер с тестируемым приложением запускается / останавливается автоматически)

Запуск smoke тестов:
```
make smoke-tests
```
Запуск всех тестов:
```
make all-tests
```


### Hexlet tests and linter status:
[![Actions Status](https://github.com/jeronymo42/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/jeronymo42/qa-auto-engineer-python-project-314/actions)