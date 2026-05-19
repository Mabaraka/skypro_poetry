from unittest.mock import patch

from main import main


def test_main_successful_json_flow(monkeypatch, capsys, mock_transaction_list):
    """Тест полного успешного сценария с выбором JSON-файла и всеми фильтрами."""

    # Имитируем ответы пользователя по шагам:
    # 1. Выбор JSON (1)
    # 2. Статус со смешанным регистром (executed) -> должен перевестись в EXECUTED
    # 3. Сортировка по дате -> Да
    # 4. Порядок сортировки -> по возрастанию
    # 5. Только рубли -> Да
    # 6. Фильтр по слову -> Да
    # 7. Слово для поиска -> Открытие
    user_inputs = ["1", "executed", "да", "по возрастанию", "да", "да", "Открытие"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    # Подменяем все импортированные функции заглушками
    with patch("main.convert_json", return_value=mock_transaction_list) as mock_json, patch(
        "main.filter_by_state", return_value=mock_transaction_list
    ), patch("main.sort_by_date", return_value=mock_transaction_list), patch(
        "main.filter_by_currency", return_value=mock_transaction_list
    ), patch(
        "main.process_bank_search", return_value=mock_transaction_list
    ), patch(
        "main.get_date", return_value="08.12.2019"
    ), patch(
        "main.mask_account_card", return_value="Счет **4321"
    ):
        main()

        # Проверяем, что функция чтения JSON вызывалась с правильным путем
        mock_json.assert_called_once_with("data/operations.json")

    # Перехватываем вывод в консоль
    captured = capsys.readouterr().out

    # Проверяем наличие ключевых строк в консоли
    assert "Привет! Добро пожаловать" in captured
    assert "Для обработки выбран JSON-файл." in captured
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured
    assert "Всего банковских операций в выборке: 1" in captured
    assert "08.12.2019 Открытие вклада" in captured


def test_main_invalid_menu_and_status_retry(monkeypatch, capsys, mock_transaction_list):
    """Тест обработки неверного ввода в меню и неверного статуса."""

    # Имитируем ошибки ввода:
    # 1. Неверный пункт меню (9) -> повтор меню
    # 2. Выбор CSV (2)
    # 3. Неверный статус (invalid_status) -> повтор ввода статуса
    # 4. Верный статус (CANCELED)
    # 5-7. Отказы от всех остальных фильтров (Нет / Нет / Нет)
    user_inputs = ["9", "2", "invalid_status", "CANCELED", "нет", "нет", "нет"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with patch("main.load_csv", return_value=mock_transaction_list) as mock_csv, patch(
        "main.filter_by_state", return_value=mock_transaction_list
    ), patch("main.get_date", return_value="12.11.2019"), patch("main.mask_account_card", return_value="Счет **1111"):
        main()
        mock_csv.assert_called_once_with("data/transactions.csv")

    captured = capsys.readouterr().out

    # Проверяем отработку ошибок
    assert "Неверный пункт меню. Попробуйте еще раз." in captured
    assert 'Статус операции "INVALID_STATUS" недоступен.' in captured
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured


def test_main_empty_result_at_start(monkeypatch, capsys):
    """Тест сценария, когда файл изначально оказался пустым."""

    # Пользователь выбирает XLSX (3), файл пустой, программа завершает работу
    user_inputs = ["3"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with patch("main.load_xlsx", return_value=[]):
        main()

    captured = capsys.readouterr().out
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured


def test_main_empty_after_filtering(monkeypatch, capsys, mock_transaction_list):
    """Тест сценария, когда после фильтрации по статусу список стал пустым."""

    # Выбираем JSON (1), вводим статус (PENDING)
    user_inputs = ["1", "PENDING"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    # Сначала данные есть, но filter_by_state возвращает пустой список
    with patch("main.convert_json", return_value=mock_transaction_list), patch(
        "main.filter_by_state", return_value=[]
    ):
        main()

    captured = capsys.readouterr().out
    assert 'Операции отфильтрованы по статусу "PENDING"' in captured
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured
