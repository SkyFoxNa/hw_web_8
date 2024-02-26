from seed import load_authors_from_file, load_qoutes_from_file
from finds import find_by_author, find_by_tag, find_by_tags


# Функція для пошуку цитат за тегом, за ім'ям автора або набором тегів
def search_quotes(command) :
    parts = command.split(':')
    if len(parts) != 2 :
        print("Неправильний формат команди")
        return

    field, value = parts[0], parts[1].strip()
    if field == 'name':
        author = find_by_author(value)
        if author:
            for a, qv in author.items():
                print(f"Автор: {a}")
                for q in qv:
                    print(f"Цитата : {q}")
        else :
            print(f"Автор не знайдений.")

    elif field == 'tag':
        quotes = find_by_tag(value)
        if quotes:
            for qv in quotes:
                print(f"Автор: {qv['author']}, Цитата: {qv['quote']}")
        else:
            print(f"Цитат не знайдено.")

    elif field == 'tags' :
        tags = value.split(',')
        tags = [tag.strip() for tag in tags]
        quotes = find_by_tags(tags)
        if quotes :
            for qv in quotes :
                print(f"Автор: {qv['author']}, Цитата: {qv['quote']}")
        else :
            print(f"Цитат не знайдено.")
    else :
        print("Непідтримувана команда")


if __name__ == '__main__':
    # Завантаження даних з файлів у відповідні колекції MongoDB
    load_authors_from_file('authors.json')
    load_qoutes_from_file('quotes.json')

    # Основний цикл для виконання команд
    while True:
        command = input("Введіть команду: ")
        if command == 'exit':
            break
        else:
            search_quotes(command)