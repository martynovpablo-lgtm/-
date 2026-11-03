"""№3: соңғы N күнтізбелік айдың орташа шығыны және нақты кэш өлшемі."""

from datetime import date
from functools import lru_cache
from time import perf_counter_ns

from core.domain import Transaction


def _sum_months(months: tuple[int, ...], cat_id: str, trans: tuple) -> int:
    """Бөліп есептеу рекурсиясы: тереңдігі log2(N)."""
    if not months:
        return 0
    if len(months) == 1:
        return sum(
            -t.amount
            for t in trans
            if t.cat_id == cat_id
            and t.amount < 0
            and date.fromisoformat(t.ts).year * 12 + date.fromisoformat(t.ts).month - 1
            == months[0]
        )
    mid = len(months) // 2
    return _sum_months(months[:mid], cat_id, trans) + _sum_months(
        months[mid:], cat_id, trans
    )


def forecast_expenses_uncached(
    cat_id: str, trans: tuple[Transaction, ...], period: int
) -> int:
    if type(period) is not int or not 1 <= period <= 120:
        raise ValueError("Ай саны 1–120 аралығында болуы керек")
    if not trans:
        return 0
    anchor = max(date.fromisoformat(t.ts) for t in trans)
    last_month = anchor.year * 12 + anchor.month - 1
    months = tuple(range(last_month - period + 1, last_month + 1))
    # Бос айлар да орташа мәнге кіреді; бүтін теңгеге төмен дөңгелектейміз.
    return _sum_months(months, cat_id, trans) // period


@lru_cache(maxsize=128, typed=True)
def forecast_expenses(cat_id: str, trans: tuple[Transaction, ...], period: int) -> int:
    return forecast_expenses_uncached(cat_id, trans, period)


def benchmark_forecast(cat_id: str, trans: tuple, period: int, repeats: int = 30):
    """Бір uncached, cold cache, кейін warm cache орташа уақыты (ms)."""
    if type(repeats) is not int or repeats < 1:
        raise ValueError("Қайталау саны оң бүтін сан болуы керек")
    forecast_expenses.cache_clear()
    start = perf_counter_ns()
    plain = forecast_expenses_uncached(cat_id, trans, period)
    uncached_ms = (perf_counter_ns() - start) / 1_000_000
    start = perf_counter_ns()
    cold = forecast_expenses(cat_id, trans, period)
    cold_ms = (perf_counter_ns() - start) / 1_000_000
    start = perf_counter_ns()
    for _ in range(repeats):
        warm = forecast_expenses(cat_id, trans, period)
    warm_ms = (perf_counter_ns() - start) / repeats / 1_000_000
    info = forecast_expenses.cache_info()
    return {
        "forecast": plain,
        "equal": plain == cold == warm,
        "uncached_ms": uncached_ms,
        "cold_ms": cold_ms,
        "warm_ms": warm_ms,
        "hits": info.hits,
        "misses": info.misses,
        "repeats": repeats,
    }
