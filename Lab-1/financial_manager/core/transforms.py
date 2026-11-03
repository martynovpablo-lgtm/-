"""№1: жаңа tuple қайтаратын функциялар және map/filter/reduce."""

import json
from dataclasses import replace
from functools import reduce
from pathlib import Path

from core.domain import Account, Budget, Category, Transaction


def load_seed(path: str | Path) -> tuple:
    """Файл оқу — I/O шекарасы. Одан кейін ядро тек immutable мәндермен жұмыс істейді."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(
        tuple(map(lambda row: model(**row), data[key]))
        for key, model in (
            ("accounts", Account),
            ("categories", Category),
            ("transactions", Transaction),
            ("budgets", Budget),
        )
    )


def add_transaction(
    trans: tuple[Transaction, ...], t: Transaction
) -> tuple[Transaction, ...]:
    if any(item.id == t.id for item in trans):
        raise ValueError("Транзакция ID-і қайталанады")
    return trans + (t,)


def update_budget(
    budgets: tuple[Budget, ...], bid: str, new_limit: int
) -> tuple[Budget, ...]:
    if type(new_limit) is not int or new_limit < 0:
        raise ValueError("Лимит теріс емес бүтін сан болуы керек")
    if not any(b.id == bid for b in budgets):
        raise ValueError("Бюджет табылмады")
    return tuple(
        map(lambda b: replace(b, limit=new_limit) if b.id == bid else b, budgets)
    )


def account_balance(trans: tuple[Transaction, ...], acc_id: str) -> int:
    """Тек транзакциялар қосындысы; бастапқы balance UI-де бөлек қосылады."""
    return reduce(
        lambda total, t: total + t.amount,
        filter(lambda t: t.account_id == acc_id, trans),
        0,
    )
