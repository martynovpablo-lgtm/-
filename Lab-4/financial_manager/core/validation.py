"""№4: күтпеген мәндер Left, жоқ категория Nothing арқылы беріледі."""

import re
from datetime import date

from core.domain import Account, Budget, Category, Transaction
from core.ftypes import Either, Maybe


def safe_category(cats: tuple[Category, ...], cat_id: str) -> Maybe[Category]:
    return Maybe(next((c for c in cats if c.id == cat_id), None))


def _error(code: str, message: str, **details):
    return Either.left({"code": code, "message": message, **details})


def valid_date(ts: str) -> bool:
    """Жарамдылық тексеруі exception қолданбайды; формат YYYY-MM-DD."""
    if not isinstance(ts, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", ts):
        return False
    year, month, day = map(int, ts.split("-"))
    if not 1 <= year <= 9999 or not 1 <= month <= 12:
        return False
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return 1 <= day <= days[month - 1]


def validate_transaction(
    t: Transaction, accs: tuple[Account, ...], cats: tuple[Category, ...]
) -> Either[dict, Transaction]:
    if not isinstance(t.id, str) or not t.id.strip():
        return _error("id", "Транзакция ID-і бос")
    account = next((a for a in accs if a.id == t.account_id), None)
    if account is None:
        return _error("account", "Шот табылмады")
    if account.currency != "KZT":
        return _error("currency", "Бұл нұсқа тек KZT қолдайды")
    category = safe_category(cats, t.cat_id)
    if not category.is_some:
        return _error("category", "Категория табылмады")
    if type(t.amount) is not int or t.amount == 0:
        return _error("amount", "Сома нөл емес бүтін теңге болуы керек")
    kind = category.value.type
    if kind not in ("income", "expense"):
        return _error("type", "Категория түрі жарамсыз")
    if (kind == "income" and t.amount < 0) or (kind == "expense" and t.amount > 0):
        return _error("sign", "Кіріс оң, шығыс теріс болуы керек")
    if not valid_date(t.ts):
        return _error("date", "Күн YYYY-MM-DD форматында және нақты болуы керек")
    if not isinstance(t.note, str):
        return _error("note", "Ескерту мәтін болуы керек")
    return Either.right(t)


def budget_usage(b: Budget, trans: tuple[Transaction, ...], anchor: str | None = None):
    """Әдепкі тірек — барлық транзакциялардың соңғы күні; енгізгенде t.ts."""
    if b.period not in ("month", "week"):
        return _error("period", "Бюджет кезеңі month немесе week болуы керек")
    if type(b.limit) is not int or b.limit < 0:
        return _error("limit", "Бюджет лимиті теріс емес бүтін сан болуы керек")
    if any(not valid_date(t.ts) for t in trans):
        return _error("date", "Транзакция күні жарамсыз")
    reference = (
        anchor if anchor is not None else max((t.ts for t in trans), default=None)
    )
    if reference is None:
        return Either.right(0)
    if not valid_date(reference):
        return _error("date", "Тірек күні жарамсыз")
    dt = date.fromisoformat(reference)
    if b.period == "month":
        matches = lambda t: t.ts[:7] == reference[:7]
    else:
        # Дүйсенбі–жексенбі; жыл шекарасында date.min үшін ordinal қолданамыз.
        monday = dt.toordinal() - dt.weekday()
        matches = lambda t: monday <= date.fromisoformat(t.ts).toordinal() < monday + 7
    return Either.right(
        sum(
            -t.amount
            for t in trans
            if t.cat_id == b.cat_id and t.amount < 0 and matches(t)
        )
    )


def check_budget(
    b: Budget, trans: tuple[Transaction, ...], anchor: str | None = None
) -> Either[dict, Budget]:
    def decide(spent):
        if spent > b.limit:
            return _error(
                "over_budget",
                "Бюджет лимиті асты",
                budget_id=b.id,
                spent=spent,
                limit=b.limit,
                excess=spent - b.limit,
            )
        return Either.right(b)

    return budget_usage(b, trans, anchor).bind(decide)


def validate_pipeline(
    t: Transaction, accs: tuple, cats: tuple, budgets: tuple, trans: tuple
):
    def unique(candidate):
        if any(old.id == candidate.id for old in trans):
            return _error("duplicate", "Транзакция ID-і қайталанады")
        return Either.right(candidate)

    def budgets_ok(candidate):
        result = Either.right(candidate)
        for b in budgets:
            if b.cat_id == candidate.cat_id:
                result = result.bind(
                    lambda current, budget=b: check_budget(
                        budget, trans + (current,), current.ts
                    ).map(lambda _: current)
                )
        return result

    return validate_transaction(t, accs, cats).bind(unique).bind(budgets_ok)
