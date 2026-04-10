# 🔐 Виджет банковских операций клиента

Утилита для маскировки номеров банковских карт и счетов, а также фильтрации и сортировки финансовых операций.

---

## 📋 Описание

Проект предоставляет набор функций для безопасной работы с финансовыми данными:

- **Маскировка** номеров карт и счетов перед отображением пользователю
- **Фильтрация** списка операций по статусу
- **Сортировка** операций по дате
- **Форматирование** дат из ISO-формата в читаемый вид

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
│   ├── masks.py       # Маскировка номеров карт и счетов
│   ├── processing.py  # Фильтрация и сортировка операций
│   └── widget.py      # Вспомогательные функции (маска + дата)
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

## 📌 Справочник функций

| Функция | Модуль | Описание |
|---|---|---|
| `get_mask_card_number(card_number)` | `masks` | Маска номера карты |
| `get_mask_account(account)` | `masks` | Маска номера счёта |
| `mask_account_card(account_card)` | `widget` | Маска по строке с типом и номером |
| `get_date(iso_date)` | `widget` | Дата из ISO в `ДД.ММ.ГГГГ` |
| `filter_by_state(data, state)` | `processing` | Фильтрация по статусу операции |
| `sort_by_date(data, reverse)` | `processing` | Сортировка по дате |

---

## 📄 Лицензия

MIT License — свободное использование и распространение.