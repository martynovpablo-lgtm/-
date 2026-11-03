import pytest

from core.domain import Category
from core.recursion import flatten_categories, sum_expenses_recursive
from core.transforms import (
    by_amount_range,
    by_category,
    by_date_range,
    filter_transactions,
)


def test_closures_remember_independent_categories(trans):
    food, salary = by_category("groceries"), by_category("salary")
    assert food(trans[0]) and not salary(trans[0])
    assert salary(trans[3]) and not food(trans[3])


def test_dates_include_boundaries(trans):
    result = filter_transactions(trans, by_date_range("2026-03-02", "2026-03-04"))
    assert tuple(t.id for t in result) == ("t2", "t3", "t4")


def test_amount_range_signed_and_inclusive(trans):
    result = filter_transactions(trans, by_amount_range(-100, -50))
    assert tuple(t.id for t in result) == ("t1", "t3", "t6")


def test_filters_combine_and_preserve_original(trans):
    assert filter_transactions(
        trans, by_category("groceries"), by_amount_range(-150, 0)
    ) == (trans[0],)
    assert len(trans) == 6
    assert filter_transactions(trans) == trans


def test_flatten_preorder_includes_root_and_grandchild(cats):
    assert tuple(c.id for c in flatten_categories(cats, "food")) == (
        "food",
        "groceries",
        "fruit",
    )
    assert tuple(c.id for c in flatten_categories(cats, "fruit")) == ("fruit",)


def test_unknown_root_and_empty_tree(cats, trans):
    assert flatten_categories(cats, "missing") == ()
    assert flatten_categories((), "food") == ()
    assert sum_expenses_recursive(cats, trans, "missing") == 0


def test_recursive_sum_includes_own_and_nested_only(cats, trans):
    assert sum_expenses_recursive(cats, trans, "food") == 375
    assert sum_expenses_recursive(cats, trans, "salary") == 0
    assert sum_expenses_recursive(cats, (), "food") == 0


@pytest.mark.parametrize("function", [flatten_categories, sum_expenses_recursive])
def test_category_cycles_rejected(function):
    cyclic = (Category("a", "A", "b", "expense"), Category("b", "B", "a", "expense"))
    with pytest.raises(ValueError, match="цикл"):
        if function is flatten_categories:
            function(cyclic, "a")
        else:
            function(cyclic, (), "a")


def test_inverted_ranges_rejected():
    with pytest.raises(ValueError):
        by_date_range("2026-03-02", "2026-01-01")
    with pytest.raises(ValueError):
        by_amount_range(10, -10)
