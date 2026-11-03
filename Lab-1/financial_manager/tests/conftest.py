from pathlib import Path

import pytest

from core.domain import Account, Budget, Category, Transaction
from core.transforms import load_seed

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def seed():
    return load_seed(ROOT / "data/seed.json")


@pytest.fixture
def accounts():
    return (Account("a1", "Шот", 1000, "KZT"), Account("a2", "Жинақ", 0, "KZT"))


@pytest.fixture
def cats():
    return (
        Category("food", "Тамақ", None, "expense"),
        Category("groceries", "Дүкен", "food", "expense"),
        Category("fruit", "Жеміс", "groceries", "expense"),
        Category("taxi", "Такси", None, "expense"),
        Category("salary", "Жалақы", None, "income"),
    )


@pytest.fixture
def trans():
    return (
        Transaction("t1", "a1", "groceries", -100, "2026-01-01", ""),
        Transaction("t2", "a1", "groceries", -200, "2026-03-02", ""),
        Transaction("t3", "a2", "fruit", -50, "2026-03-03", ""),
        Transaction("t4", "a1", "salary", 1000, "2026-03-04", ""),
        Transaction("t5", "a1", "food", -25, "2026-03-05", ""),
        Transaction("t6", "a1", "taxi", -75, "2026-03-06", ""),
    )


@pytest.fixture
def budgets():
    return (Budget("b1", "groceries", 300, "month"), Budget("b2", "taxi", 100, "week"))
