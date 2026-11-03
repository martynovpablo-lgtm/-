from dataclasses import FrozenInstanceError

import pytest

from core.domain import Event, Transaction
from core.transforms import account_balance, add_transaction, update_budget


def test_seed_minimum_and_immutable_collections(seed):
    assert isinstance(seed, tuple)
    assert all(isinstance(group, tuple) for group in seed)
    assert all(len(group) >= limit for group, limit in zip(seed, (3, 10, 100, 3)))


def test_all_domain_models_are_frozen(seed):
    for group in seed:
        with pytest.raises(FrozenInstanceError):
            group[0].id = "changed"


def test_seed_references_and_unique_ids(seed):
    accounts, cats, transactions, budgets = seed
    for group in seed:
        assert len({item.id for item in group}) == len(group)
    aids, cids = {a.id for a in accounts}, {c.id for c in cats}
    assert all(t.account_id in aids and t.cat_id in cids for t in transactions)
    assert all(c.parent_id is None or c.parent_id in cids for c in cats)
    assert all(b.cat_id in cids and b.limit >= 0 for b in budgets)


def test_add_returns_new_collection_without_mutation(trans):
    before = tuple(trans)
    t = Transaction("new", "a1", "salary", 10, "2026-03-10", "")
    after = add_transaction(trans, t)
    assert trans == before
    assert after == before + (t,) and after is not trans


def test_duplicate_transaction_rejected(trans):
    with pytest.raises(ValueError, match="қайталанады"):
        add_transaction(trans, trans[0])


def test_update_budget_preserves_input_and_other_budgets(budgets):
    updated = update_budget(budgets, "b1", 0)
    assert budgets[0].limit == 300 and updated[0].limit == 0
    assert updated[1] is budgets[1]


@pytest.mark.parametrize(
    "bid,limit", [("missing", 100), ("b1", -1), ("b1", True), ("b1", 2.5)]
)
def test_invalid_budget_update(budgets, bid, limit):
    with pytest.raises(ValueError):
        update_budget(budgets, bid, limit)


def test_reduce_balance_sign_and_account_filter(trans):
    assert account_balance(trans, "a1") == 600
    assert account_balance(trans, "a2") == -50


def test_empty_and_unknown_account_balance(trans):
    assert account_balance((), "a1") == 0
    assert account_balance(trans, "missing") == 0


def test_event_payload_is_deeply_frozen():
    source = {"nested": {"values": [1, 2]}}
    event = Event("e1", "2026-01-01", "TRANSACTION_ADDED", source)
    source["nested"]["values"].append(3)
    assert event.payload["nested"]["values"] == (1, 2)
    with pytest.raises(TypeError):
        event.payload["nested"]["values"] = ()
