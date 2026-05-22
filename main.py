from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_TITLE = 'Учёт посещённых мест'
DATA_FILE = Path(__file__).with_name('places.json')
FIELDS = [{'name': 'city', 'label': 'Город', 'type': 'text', 'sample': 'Прага'}, {'name': 'country', 'label': 'Страна', 'type': 'text', 'sample': 'Чехия'}, {'name': 'date', 'label': 'Дата посещения', 'type': 'text', 'sample': '2026-05-21'}, {'name': 'rating', 'label': 'Оценка поездки от 1 до 5', 'type': 'int', 'sample': 5, 'min': 1, 'max': 5}]
GROUP_FIELD = 'country'
NUMERIC_FIELD = 'rating'
NUMERIC_LABEL = 'Средняя оценка поездок'
NUMERIC_MODE = 'average'
DUPLICATE_FIELDS = ['city', 'country', 'date']
SAMPLE_RECORD = {'city': 'Прага', 'country': 'Чехия', 'date': '2026-05-21', 'rating': 5}


def load_records() -> list[dict[str, Any]]:
    """Загружает записи из JSON-файла."""
    if not DATA_FILE.exists():
        return []
    try:
        content = DATA_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
        if isinstance(data, list):
            return data
        raise ValueError("JSON-файл должен содержать список записей")
    except json.JSONDecodeError as error:
        raise ValueError(f"Ошибка чтения JSON: {error}") from error


def save_records(records: list[dict[str, Any]]) -> None:
    """Сохраняет записи в JSON-файл."""
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_value(field: dict[str, Any], raw_value: str) -> Any:
    """Проверяет и преобразует пользовательский ввод."""
    value = raw_value.strip()
    if not value:
        raise ValueError(f"Поле '{field['label']}' не должно быть пустым")

    field_type = field.get("type", "text")
    if field_type == "text":
        return value

    if field_type == "choice":
        choices = field.get("choices", [])
        if value not in choices:
            raise ValueError(f"Допустимые значения: {', '.join(choices)}")
        return value

    if field_type == "int":
        try:
            number = int(value)
        except ValueError as error:
            raise ValueError("Нужно ввести целое число") from error
        if "min" in field and field["min"] is not None and number < field["min"]:
            raise ValueError(f"Минимальное значение: {field['min']}")
        if "max" in field and field["max"] is not None and number > field["max"]:
            raise ValueError(f"Максимальное значение: {field['max']}")
        return number

    if field_type == "float":
        normalized = value.replace(",", ".")
        try:
            number = float(normalized)
        except ValueError as error:
            raise ValueError("Нужно ввести число") from error
        if "min" in field and field["min"] is not None and number < field["min"]:
            raise ValueError(f"Минимальное значение: {field['min']}")
        if "max" in field and field["max"] is not None and number > field["max"]:
            raise ValueError(f"Максимальное значение: {field['max']}")
        return number

    return value


def is_duplicate(records: list[dict[str, Any]], new_record: dict[str, Any]) -> bool:
    """Проверяет дубликат по ключевым полям проекта."""
    if not DUPLICATE_FIELDS:
        return False
    for record in records:
        if all(str(record.get(field, "")).lower() == str(new_record.get(field, "")).lower() for field in DUPLICATE_FIELDS):
            return True
    return False


def add_record_interactive(records: list[dict[str, Any]]) -> None:
    """Добавляет новую запись через консольный ввод."""
    print(f"\nДобавление записи: {PROJECT_TITLE}")
    new_record: dict[str, Any] = {}
    for field in FIELDS:
        while True:
            try:
                raw_value = input(f"{field['label']}: ")
                new_record[field["name"]] = parse_value(field, raw_value)
                break
            except ValueError as error:
                print(f"Ошибка: {error}")

    if is_duplicate(records, new_record):
        print("Такая запись уже есть. Добавление отменено.")
        return

    records.append(new_record)
    save_records(records)
    print("Запись добавлена.")


def format_record(record: dict[str, Any], index: int) -> str:
    """Форматирует запись для вывода в консоль."""
    parts = []
    for field in FIELDS:
        name = field["name"]
        parts.append(f"{field['label']}: {record.get(name, '')}")
    return f"{index}. " + " | ".join(parts)


def list_records(records: list[dict[str, Any]]) -> None:
    """Показывает все записи."""
    if not records:
        print("Список пуст.")
        return
    for index, record in enumerate(records, start=1):
        print(format_record(record, index))


def count_by_field(records: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    """Считает количество записей по указанному полю."""
    result: dict[str, int] = {}
    for record in records:
        key = str(record.get(field_name, "Не указано"))
        result[key] = result.get(key, 0) + 1
    return result


def calculate_average(records: list[dict[str, Any]], field_name: str) -> float:
    """Считает среднее значение числового поля."""
    values = [float(record[field_name]) for record in records if field_name in record]
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_sum(records: list[dict[str, Any]], field_name: str) -> float:
    """Считает сумму числового поля."""
    return sum(float(record[field_name]) for record in records if field_name in record)


def show_stats(records: list[dict[str, Any]]) -> None:
    """Показывает статистику проекта."""
    if not records:
        print("Нет данных для статистики.")
        return

    print(f"\nВсего записей: {len(records)}")
    print(f"Статистика по полю '{GROUP_FIELD}':")
    for key, value in count_by_field(records, GROUP_FIELD).items():
        print(f"- {key}: {value}")

    if NUMERIC_FIELD:
        if NUMERIC_MODE == "sum":
            value = calculate_sum(records, NUMERIC_FIELD)
        else:
            value = calculate_average(records, NUMERIC_FIELD)
        print(f"{NUMERIC_LABEL}: {value:.2f}")


def delete_record_by_index(records: list[dict[str, Any]], index: int) -> dict[str, Any]:
    """Удаляет запись по номеру и возвращает удаленный элемент."""
    if index < 1 or index > len(records):
        raise IndexError("Нет записи с таким номером")
    return records.pop(index - 1)


def delete_record_interactive(records: list[dict[str, Any]]) -> None:
    """Удаляет запись через консольный ввод."""
    if not records:
        print("Удалять нечего: список пуст.")
        return
    list_records(records)
    try:
        index = int(input("Введите номер записи для удаления: "))
        removed = delete_record_by_index(records, index)
    except ValueError:
        print("Нужно ввести число.")
        return
    except IndexError as error:
        print(f"Ошибка: {error}")
        return
    save_records(records)
    print(f"Удалена запись: {removed}")


def print_menu() -> None:
    print(f"\n{PROJECT_TITLE}")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Показать статистику")
    print("4. Удалить запись")
    print("5. Выход")


def main() -> None:
    records = load_records()
    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            add_record_interactive(records)
        elif choice == "2":
            list_records(records)
        elif choice == "3":
            show_stats(records)
        elif choice == "4":
            delete_record_interactive(records)
        elif choice == "5":
            print("Выход.")
            break
        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
