# 🔐 Виджет банковских операций клиента

Утилита для маскировки номеров банковских карт и счетов, а также фильтрации, сортировки, генерации финансовых операций и логирования вызовов функций.

---

## 📋 Описание

Проект предоставляет набор функций для безопасной работы с финансовыми данными:

- **Маскировка** номеров карт и счетов перед отображением пользователю
- **Фильтрация** списка операций по статусу
- **Сортировка** операций по дате
- **Форматирование** дат из ISO-формата в читаемый вид
- **Генерация** номеров карт, итерация по транзакциям и их описаниям
- **Логирование** вызовов функций в консоль или файл через декоратор

---

## ⚙️ Установка

### Требования

- Python 3.8+

### Клонирование репозитория

```bash
git clone https://github.com/username/your-repo.git
cd your-repo
```

### Установка зависимостей

Проект использует только стандартную библиотеку Python — дополнительная установка пакетов не требуется.

---

## 📁 Структура проекта

```
your-repo/
├── src/
│   ├── masks.py         # Маскировка номеров карт и счетов
│   ├── processing.py    # Фильтрация и сортировка операций
│   ├── widget.py        # Вспомогательные функции (маска + дата)
│   ├── generators.py    # Генераторы для итерации по транзакциям
│   └── decorators.py    # Декоратор логирования
├── tests/
│   ├── conftest.py      # Фикстуры для всех тестов
│   ├── test_masks.py    # Тесты модуля masks
│   ├── test_processing.py  # Тесты модуля processing
│   ├── test_widget.py   # Тесты модуля widget
│   ├── test_generators.py  # Тесты модуля generators
│   └── test_decorators.py  # Тесты модуля decorators
└── README.md
```

---

## 🚀 Использование

### Маскировка номера карты

```python
from src.masks import get_mask_card_number

get_mask_card_number(7000792289606361)
# → "7000 79** **** 6361"
```

Формат вывода: `XXXX XX** **** XXXX` — видны первые 6 и последние 4 цифры.

---

### Маскировка номера счёта

```python
from src.masks import get_mask_account

get_mask_account(73654108430135874305)
# → "**4305"
```

Формат вывода: `**XXXX` — видны только последние 4 цифры.

---

### Маскировка карты или счёта по строке

```python
from src.widget import mask_account_card

mask_account_card("Visa Platinum 7000792289606361")
# → "Visa Platinum 7000 79** **** 6361"

mask_account_card("Счет 73654108430135874305")
# → "Счет **4305"
```

Функция автоматически определяет тип (карта или счёт) и применяет нужную маску.

---

### Форматирование даты

```python
from src.widget import get_date

get_date("2024-03-11T02:26:18.671407")
# → "11.03.2024"
```

Принимает дату в формате ISO 8601, возвращает строку `ДД.ММ.ГГГГ`.

---

### Фильтрация операций по статусу

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED", "amount": 500},
    {"id": 2, "state": "CANCELLED", "amount": 200},
    {"id": 3, "state": "EXECUTED", "amount": 150},
]

filter_by_state(operations)
# → [{"id": 1, ...}, {"id": 3, ...}]

filter_by_state(operations, state="CANCELLED")
# → [{"id": 2, ...}]
```

По умолчанию фильтрует по статусу `EXECUTED`.

---

### Сортировка операций по дате

```python
from src.processing import sort_by_date

operations = [
    {"id": 1, "date": "2024-01-15", "amount": 500},
    {"id": 2, "date": "2024-03-01", "amount": 200},
    {"id": 3, "date": "2023-12-20", "amount": 150},
]

sort_by_date(operations)
# → от новых к старым: id 2 → id 1 → id 3

sort_by_date(operations, reverse=False)
# → от старых к новым: id 3 → id 1 → id 2
```

По умолчанию сортировка идёт от новых к старым (`reverse=True`).

---

### Фильтрация транзакций по валюте

```python
from src.generators import filter_by_currency

transactions = [
    {
        "id": 1,
        "description": "Перевод организации",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 2,
        "description": "Социальный перевод",
        "operationAmount": {"amount": "30242.83", "currency": {"name": "руб.", "code": "RUB"}},
    },
    {
        "id": 3,
        "description": "Перевод со счета на счет",
        "operationAmount": {"amount": "150.00", "currency": {"name": "USD", "code": "USD"}},
    },
]

usd_transactions = filter_by_currency(transactions, "USD")
for t in usd_transactions:
    print(t["id"])
# → 1
# → 3
```

Функция возвращает генератор, который поочерёдно выдаёт только те транзакции, в которых код валюты совпадает с заданным. Транзакции с отсутствующим или некорректным полем валюты пропускаются.

---

### Получение описаний транзакций

```python
from src.generators import transaction_descriptions

transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Открытие вклада"},
    {"id": 3, "description": "Перевод со счета на счет"},
]

descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # → "Перевод организации"
print(next(descriptions))  # → "Открытие вклада"
print(next(descriptions))  # → "Перевод со счета на счет"
```

Функция возвращает генератор, который поочерёдно выдаёт строку `description` из каждой транзакции. Транзакции без поля `description` пропускаются.

---

### Генератор номеров банковских карт

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# → "0000 0000 0000 0001"
# → "0000 0000 0000 0002"
# → "0000 0000 0000 0003"
# → "0000 0000 0000 0004"
# → "0000 0000 0000 0005"

# Конкретный диапазон
for card in card_number_generator(9999999999999998, 9999999999999999):
    print(card)
# → "9999 9999 9999 9998"
# → "9999 9999 9999 9999"
```

Генерирует номера карт в формате `XXXX XXXX XXXX XXXX` в заданном диапазоне от `0000 0000 0000 0001` до `9999 9999 9999 9999`. Если `start > end`, генератор не выдаёт ни одного значения.

---

### Логирование вызовов функций

```python
from src.decorators import log

# Вывод в консоль
@log()
def add(a, b):
    return a + b

add(1, 2)
# stdout → "add ok"

# При ошибке
@log()
def divide(a, b):
    return a / b

divide(1, 0)
# stdout → "divide error: division by zero. Inputs: (1, 0), {}"
# затем пробрасывает ZeroDivisionError дальше
```

```python
# Запись в файл
@log("operations.log")
def add(a, b):
    return a + b

add(1, 2)
# operations.log → "add ok"
```

Декоратор `log` принимает необязательный аргумент `filename`. Если он передан — сообщения дописываются в файл, иначе выводятся в `stdout`. При исключении в лог записывается текст ошибки и входные параметры, после чего исключение пробрасывается дальше. Оригинальное имя функции сохраняется через `@wraps`.

---

## 🧪 Тестирование

### Запуск тестов

```bash
pytest
```

С отчётом о покрытии:

```bash
pytest --cov=src --cov-report=term-missing
```

### Установка зависимостей для тестирования

```bash
pip install pytest pytest-cov
```

---

### Структура тестов

Тесты покрывают все публичные функции проекта и организованы по пяти файлам, соответствующим модулям `src/`.

**`conftest.py`** содержит общие фикстуры, переиспользуемые всеми тест-файлами:

| Фикстура | Описание |
|---|---|
| `empty_transactions` | Пустой список операций |
| `sample_transactions` | Список из 6 операций с разными статусами |
| `transactions_without_state` | Операции, у части которых отсутствует ключ `state` |
| `transactions_for_sort` | Операции с разными датами для проверки сортировки |
| `transactions_with_bad_dates` | Смесь валидных, невалидных дат и отсутствующих ключей |
| `transactions_datetime_objects` | Операции, где `date` — объект `datetime` |
| `transactions_with_currency` | Операции с полем `operationAmount.currency` для фильтрации по валюте |
| `transaction_with_descriptions` | Операции с полем `description` для проверки генератора описаний |

---

**`test_processing.py`** — тесты фильтрации и сортировки:

| Тест | Что проверяет |
|---|---|
| `test_filter_parametrized` | Фильтрацию по статусам `EXECUTED`, `PENDING`, `CANCELED`, несуществующим и пустой строке |
| `test_filter_default_state` | Что параметр `state` по умолчанию равен `EXECUTED` |
| `test_filter_empty_list` | Поведение на пустом списке |
| `test_filter_missing_state_key` | Что элементы без ключа `state` не попадают в результат |
| `test_filter_does_not_mutate` | Что функция не изменяет исходный список |
| `test_sort_parametrized` | Сортировку по убыванию и возрастанию |
| `test_sort_default_is_descending` | Что `reverse=True` по умолчанию |
| `test_sort_empty_list` | Поведение на пустом списке |
| `test_sort_bad_dates_go_last` | Что записи с невалидными или отсутствующими датами уходят в конец |
| `test_sort_datetime_objects` | Корректную работу, когда `date` — объект `datetime` |
| `test_sort_does_not_mutate` | Что функция не изменяет исходный список |

---

**`test_widget.py`** — тесты маскировки и форматирования дат:

| Тест | Что проверяет |
|---|---|
| `test_mask_account_card` | Маскировку счетов, карт и обработку невалидного ввода (параметризованный) |
| `test_get_date_valid` | Корректное форматирование валидных ISO-дат: простая дата, со временем, с миллисекундами, с таймзоной, високосный год, начало и конец года |
| `test_get_date_invalid` | Что невалидный ввод возвращает строку с ошибкой, а не выбрасывает исключение |
| `test_get_date_none` | Обработку `None` вместо строки |
| `test_get_date_output_format` | Структуру вывода `ДД.ММ.ГГГГ` (длина, разделители, порядок компонентов) |

---

**`test_generators.py`** — тесты генераторов:

| Тест | Что проверяет |
|---|---|
| `test_filter_by_currency` | Фильтрацию по кодам валют `USD`, `EUR`, `RUB` (параметризованный) |
| `test_filter_by_currency_empty_list` | Поведение на пустом списке |
| `test_transaction_descriptions` | Последовательную выдачу описаний через `next()` |
| `test_transaction_descriptions_empty_list` | Что на пустом списке сразу бросается `StopIteration` |
| `test_card_number_generator` | Генерацию в диапазонах: начало, конец, одно значение, максимальное число, `start > end` (параметризованный) |

---

**`test_decorators.py`** — тесты декоратора логирования:

| Тест | Что проверяет |
|---|---|
| `test_log_successful` | Вывод `"<name> ok"` в stdout при успешном вызове и корректный возврат результата |
| `test_log_failed` | Вывод сообщения об ошибке с входными параметрами при исключении (параметризованный: args и kwargs) |
| `test_log_successful_with_filename` | Запись `"<name> ok"` в файл при успешном вызове |
| `test_log_failed_with_filename` | Запись сообщения об ошибке в файл при исключении (параметризованный: args и kwargs) |
| `test_log_invalid_path` | Что `FileNotFoundError` пробрасывается, если путь к лог-файлу не существует |

---

## 📌 Справочник функций

| Функция | Модуль | Описание |
|---|---|---|
| `get_mask_card_number(card_number)` | `masks` | Маска номера карты |
| `get_mask_account(account)` | `masks` | Маска номера счёта |
| `mask_account_card(account_card)` | `widget` | Маска по строке с типом и номером |
| `get_date(iso_date)` | `widget` | Дата из ISO в `ДД.ММ.ГГГГ` |
| `filter_by_state(data, state)` | `processing` | Фильтрация по статусу операции |
| `sort_by_date(data, reverse)` | `processing` | Сортировка по дате |
| `filter_by_currency(transactions, currency)` | `generators` | Генератор транзакций с заданной валютой |
| `transaction_descriptions(transactions)` | `generators` | Генератор описаний транзакций |
| `card_number_generator(start, end)` | `generators` | Генератор номеров карт в формате `XXXX XXXX XXXX XXXX` |
| `log(filename)` | `decorators` | Декоратор логирования вызовов в консоль или файл |

---

## 📄 Лицензия

MIT License — свободное использование и распространение.