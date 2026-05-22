# Git/GitHub steps для проекта «Учёт посещённых мест»

```bash
git init
git branch -M main
git add README.md .gitignore main.py places.json tests/test_app.py
git commit -m "Создать базовую структуру проекта"
git remote add origin https://github.com/pipelineOfProjects1t/team-python-github.git
git push -u origin main
```

## Ветка добавления записи

```bash
git checkout -b feature/add-record
# доработать функцию add_record_interactive
git add .
git commit -m "Добавить функцию добавления записи. Closes #1"
git push -u origin feature/add-record
```

После пуша нужно создать Pull Request на GitHub:

- base: `main`
- compare: `feature/add-record`
- описание: что добавлена функция добавления записи и проверка ввода.

## Остальные ветки

```bash
git checkout main
git pull
git checkout -b feature/list-and-stats
# доработать вывод списка и статистику
git add .
git commit -m "Добавить список и статистику"
git checkout main
git merge feature/list-and-stats

git checkout -b feature/delete-record
# доработать удаление записи
git add .
git commit -m "Добавить удаление записи"
git checkout main
git merge feature/delete-record
git push
```

## Проверка графа коммитов

```bash
git log --oneline --graph --all
```
