"""Ақша бүтін теңгемен сақталады; кіріс оң, шығыс теріс."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class Account:
    id: str
    name: str
    balance: int
    currency: str


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    parent_id: str | None
    type: str


@dataclass(frozen=True)
class Transaction:
    id: str
    account_id: str
    cat_id: str
    amount: int
    ts: str
    note: str


@dataclass(frozen=True)
class Budget:
    id: str
    cat_id: str
    limit: int
    period: str


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(map(_freeze, value))
    if isinstance(value, set):
        return frozenset(map(_freeze, value))
    return value


@dataclass(frozen=True)
class Event:
    id: str
    ts: str
    name: str
    payload: Mapping

    def __post_init__(self):
        object.__setattr__(self, "payload", _freeze(dict(self.payload)))
