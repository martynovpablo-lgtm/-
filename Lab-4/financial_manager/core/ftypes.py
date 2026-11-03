"""№4: None — Nothing; Either күйі бөлек сақталады, Right(None) жарамды."""

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


@dataclass(frozen=True)
class Maybe(Generic[T]):
    value: T | None = None

    @property
    def is_some(self) -> bool:
        return self.value is not None

    def map(self, fn: Callable[[T], U]) -> "Maybe[U]":
        return Maybe(fn(self.value)) if self.is_some else Maybe()

    def bind(self, fn: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        return fn(self.value) if self.is_some else Maybe()

    def get_or_else(self, default):
        return self.value if self.is_some else default


@dataclass(frozen=True)
class Either(Generic[E, T]):
    is_right: bool
    value: E | T

    @classmethod
    def right(cls, value):
        return cls(True, value)

    @classmethod
    def left(cls, error):
        return cls(False, error)

    def map(self, fn: Callable[[T], U]) -> "Either[E, U]":
        return Either.right(fn(self.value)) if self.is_right else self

    def bind(self, fn: Callable[[T], "Either[E, U]"]) -> "Either[E, U]":
        return fn(self.value) if self.is_right else self

    def get_or_else(self, default):
        return self.value if self.is_right else default
