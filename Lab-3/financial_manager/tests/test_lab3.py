import pytest

from core.domain import Transaction
from core.memo import benchmark_forecast, forecast_expenses, forecast_expenses_uncached


def test_forecast_includes_zero_month_and_integer_rounding(trans):
    # Қаңтар 100, ақпан 0, наурыз 200 → 300 // 3.
    assert forecast_expenses("groceries", trans, 3) == 100
    assert forecast_expenses("groceries", trans, 2) == 100
    assert forecast_expenses("groceries", trans, 1) == 200


def test_empty_missing_and_income_category(trans):
    assert forecast_expenses("groceries", (), 3) == 0
    assert forecast_expenses("missing", trans, 3) == 0
    assert forecast_expenses("salary", trans, 3) == 0


def test_cold_and_warm_cache_hits(trans):
    forecast_expenses.cache_clear()
    assert forecast_expenses("groceries", trans, 3) == 100
    assert forecast_expenses.cache_info().misses == 1
    assert forecast_expenses("groceries", trans, 3) == 100
    assert forecast_expenses.cache_info().hits == 1


def test_cache_key_changes_with_new_immutable_transactions(trans):
    forecast_expenses.cache_clear()
    updated = trans + (Transaction("new", "a1", "groceries", -300, "2026-03-07", ""),)
    assert forecast_expenses("groceries", trans, 3) == 100
    assert forecast_expenses("groceries", updated, 3) == 200
    assert forecast_expenses.cache_info().misses == 2
    assert len(trans) == 6


def test_cache_key_includes_category_and_period(trans):
    forecast_expenses.cache_clear()
    forecast_expenses("groceries", trans, 3)
    forecast_expenses("groceries", trans, 1)
    forecast_expenses("taxi", trans, 3)
    assert forecast_expenses.cache_info().misses == 3


@pytest.mark.parametrize("period", [0, -1, 121, True, 2.5])
def test_invalid_period_rejected(trans, period):
    with pytest.raises(ValueError):
        forecast_expenses("groceries", trans, period)


def test_recursion_month_window_crosses_year_and_excludes_old_month():
    transactions = (
        Transaction("1", "a1", "c", -500, "2025-11-30", ""),
        Transaction("2", "a1", "c", -120, "2025-12-31", ""),
        Transaction("3", "a1", "c", -81, "2026-01-01", ""),
    )
    assert forecast_expenses("c", transactions, 2) == 100


def test_timing_real_nonnegative_and_correct_cache_counts(trans):
    result = benchmark_forecast("groceries", trans, 3, repeats=7)
    assert result["forecast"] == 100 and result["equal"]
    assert all(result[key] >= 0 for key in ("uncached_ms", "cold_ms", "warm_ms"))
    assert result["hits"] == 7 and result["misses"] == 1


def test_cached_uncached_equal_for_all_seed_categories(seed):
    _, cats, transactions, _ = seed
    for cat in cats:
        assert forecast_expenses(cat.id, transactions, 6) == forecast_expenses_uncached(
            cat.id, transactions, 6
        )
