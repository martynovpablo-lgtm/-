"""Бірдей 180 транзакцияны қайта жасау: python data/generate_seed.py."""

import json
from pathlib import Path


def build_seed():
    categories = [
        ("food", "Тамақтану", None, "expense"),
        ("groceries", "Азық-түлік", "food", "expense"),
        ("cafe", "Кафе", "food", "expense"),
        ("transport", "Көлік", None, "expense"),
        ("bus", "Автобус", "transport", "expense"),
        ("taxi", "Такси", "transport", "expense"),
        ("leisure", "Демалыс", None, "expense"),
        ("cinema", "Кино", "leisure", "expense"),
        ("books", "Кітаптар", "leisure", "expense"),
        ("sport", "Спорт", "leisure", "expense"),
        ("home", "Үй", None, "expense"),
        ("utilities", "Коммуналдық төлем", "home", "expense"),
        ("income", "Кіріс", None, "income"),
        ("salary", "Жалақы", "income", "income"),
        ("bonus", "Сыйақы", "income", "income"),
    ]
    expense_ids = (
        "groceries",
        "cafe",
        "bus",
        "taxi",
        "cinema",
        "books",
        "sport",
        "utilities",
        "food",
    )
    transactions = []
    for month in range(4, 10):
        for index in range(30):
            income = index < 3
            cid = "salary" if income else expense_ids[(index - 3) % len(expense_ids)]
            amount = (
                120000 + month * 1000
                if income
                else -(1000 + ((month * 31 + index * 17) % 50) * 100)
            )
            transactions.append(
                {
                    "id": f"t-{month:02d}-{index:02d}",
                    "account_id": f"a{index % 3 + 1}",
                    "cat_id": cid,
                    "amount": amount,
                    "ts": f"2026-{month:02d}-{index % 28 + 1:02d}",
                    "note": "Жалақы" if income else "Үлгі шығын",
                }
            )
    return {
        "accounts": [
            {"id": "a1", "name": "Негізгі шот", "balance": 50000, "currency": "KZT"},
            {"id": "a2", "name": "Қолма-қол", "balance": 20000, "currency": "KZT"},
            {"id": "a3", "name": "Жинақ", "balance": 100000, "currency": "KZT"},
        ],
        "categories": [
            dict(zip(("id", "name", "parent_id", "type"), row)) for row in categories
        ],
        "transactions": transactions,
        "budgets": [
            {"id": "b1", "cat_id": "groceries", "limit": 18000, "period": "month"},
            {"id": "b2", "cat_id": "taxi", "limit": 5000, "period": "week"},
            {"id": "b3", "cat_id": "cinema", "limit": 8000, "period": "month"},
        ],
    }


if __name__ == "__main__":
    destination = Path(__file__).with_name("seed.json")
    destination.write_text(
        json.dumps(build_seed(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Дайын: {destination.name}; 3 шот, 15 категория, 180 транзакция, 3 бюджет")
