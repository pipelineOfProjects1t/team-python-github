import json
from collections import Counter
from pathlib import Path

DATA_FILE = Path("books.json")


def load_books():
    """Загружает список книг из JSON-файла."""
    if not DATA_FILE.exists():
        return []
    try:
        content = DATA_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print("Ошибка: файл books.json повреждён. Будет использован пустой список.")
        return []


def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    DATA_FILE.write_text(
        json.dumps(books, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def normalize(value):
    """Нормализует строку для сравнения."""
    return value.strip().lower()


def is_duplicate(books, author, title):
    """Проверяет, есть ли уже такая книга по автору и названию."""
    author = normalize(author)
    title = normalize(title)
    return any(
        normalize(book.get("author", "")) == author and
        normalize(book.get("title", "")) == title
        for book in books
    )


def calculate_average_rating(books):
    """Возвращает среднюю оценку книг."""
    if not books:
        return 0
    return sum(book["rating"] for book in books) / len(books)


def count_books_by_author(books):
    """Возвращает статистику количества книг по авторам."""
    return Counter(book["author"] for book in books)


def input_not_empty(prompt):
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не должно быть пустым.")


def input_rating():
    """Запрашивает оценку от 1 до 5."""
    while True:
        try:
            rating = int(input("Оценка от 1 до 5: "))
            if 1 <= rating <= 5:
                return rating
            print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите целое число от 1 до 5.")


def add_book(books):
    """Добавляет новую книгу."""
    print("\nДобавление книги")
    author = input_not_empty("Автор: ")
    title = input_not_empty("Название: ")

    if is_duplicate(books, author, title):
        print("Такая книга уже есть в списке.")
        return books

    rating = input_rating()
    read_date = input_not_empty("Дата прочтения: ")

    books.append({
        "author": author,
        "title": title,
        "rating": rating,
        "read_date": read_date
    })
    save_books(books)
    print("Книга добавлена.")
    return books


def show_books(books):
    """Показывает все книги."""
    print("\nСписок книг")
    if not books:
        print("Список пока пуст.")
        return

    for index, book in enumerate(books, start=1):
        print(
            f"{index}. {book['author']} — {book['title']} | "
            f"оценка: {book['rating']} | дата: {book['read_date']}"
        )


def show_average_rating(books):
    """Показывает среднюю оценку."""
    print("\nСредняя оценка")
    if not books:
        print("Пока нет книг для расчёта.")
        return
    print(f"Средняя оценка: {calculate_average_rating(books):.2f}")


def show_author_stats(books):
    """Показывает статистику по авторам."""
    print("\nСтатистика по авторам")
    if not books:
        print("Пока нет данных для статистики.")
        return

    stats = count_books_by_author(books)
    for author, count in stats.items():
        print(f"{author}: {count}")


def delete_book(books):
    """Удаляет книгу по номеру в списке."""
    print("\nУдаление книги")
    if not books:
        print("Список пуст, удалять нечего.")
        return books

    show_books(books)
    try:
        index = int(input("Введите номер книги для удаления: "))
        if 1 <= index <= len(books):
            removed = books.pop(index - 1)
            save_books(books)
            print(f"Удалена книга: {removed['author']} — {removed['title']}")
        else:
            print("Книги с таким номером нет.")
    except ValueError:
        print("Нужно ввести число.")
    return books


def show_menu():
    """Показывает главное меню."""
    print("\nТрекер прочитанных книг")
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Показать среднюю оценку")
    print("4. Статистика по авторам")
    print("5. Удалить книгу")
    print("6. Выход")


def main():
    books = load_books()

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            books = add_book(books)
        elif choice == "2":
            show_books(books)
        elif choice == "3":
            show_average_rating(books)
        elif choice == "4":
            show_author_stats(books)
        elif choice == "5":
            books = delete_book(books)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
