from src.generators import filter_by_currency
from src.processing import filter_by_state
from src.processing import sort_by_date
from src.search import process_bank_search
from src.transactions_reader import load_csv
from src.transactions_reader import load_xlsx
from src.utils import convert_json
from src.widget import get_date
from src.widget import mask_account_card


def main() -> None:
    """Основная функция для управления логикой приложения с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор источника данных
    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            transactions = convert_json("data/operations.json")
            break
        elif choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            transactions = load_csv("data/transactions.csv")
            break
        elif choice == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            transactions = load_xlsx("data/transactions_excel.xlsx")
            break
        else:
            print("Программа: Неверный пункт меню. Попробуйте еще раз.")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 2. Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Пользователь: ").strip().upper()

        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'Программа: Операции отфильтрованы по статусу "{status_input}"')
            break
        else:
            print(f'Программа: Статус операции "{status_input}" недоступен.')

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка по дате
    print("Программа: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("Пользователь: ").strip().lower()
    if sort_choice == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("Пользователь: ").strip().lower()
        descending = True if "убыван" in order_choice else False
        transactions = sort_by_date(transactions, descending=descending)

    # 4. Фильтрация по валюте (только рубли)
    print("Программа: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Пользователь: ").strip().lower()
    if rub_choice == "да":
        transactions = filter_by_currency(transactions, "RUB")

    # 5. Фильтрация по слову в описании
    print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    desc_choice = input("Пользователь: ").strip().lower()
    if desc_choice == "да":
        search_word = input("Пользователь (введите слово): ").strip()
        transactions = process_bank_search(list(transactions), search_word)

    # 6. Вывод результатов
    print("Программа: Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(list(transactions))}")
    for tx in transactions:
        date = get_date(tx.get("date", ""))
        description = tx.get("description", "")
        from_info = mask_account_card(tx.get("from", ""))
        to_info = mask_account_card(tx.get("to", ""))

        amount = tx.get("operationAmount", {}).get("amount", "")
        currency = tx.get("operationAmount", {}).get("currency", {}).get("name", "")

        transfer_route = f"{from_info} -> {to_info}"
        print(f"{date} {description}\n{transfer_route}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
