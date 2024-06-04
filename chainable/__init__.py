from __future__ import annotations

from itertools import chain
from functools import reduce, _initial_missing
from typing import TypeVar, Callable, overload, Generic, Any
from collections.abc import Iterable, Iterator

__all__ = ("Chainable",)

T = TypeVar("T")
S = TypeVar("S")


class Chainable(Generic[T]):
    def __init__(self, it: Iterable[T]) -> None:
        self.it = it

    def __iter__(self) -> Iterator[T]:
        return iter(self.it)

    def map(self, mapper: Callable[[T], S]) -> Chainable[S]:
        return Chainable(map(mapper, self))
    
    def filter(self, predicate: Callable[[T], bool]) -> Chainable[T]:
        return Chainable(filter(predicate, self))
    
    @overload
    def reduce(self, reducer: Callable[[T, T], T]) -> T:
        ...
    
    @overload
    def reduce(self, reducer: Callable[[T, T], T], initial: T) -> T:
        ...

    def reduce(self, reducer, initial = _initial_missing) -> T:
        return reduce(reducer, self, _initial_missing)

    def any(self, pred: Callable[[T], Any] = lambda x: x) -> bool:
        return any(self.map(pred))
    
    def all(self, pred: Callable[[T], Any] = lambda x: x) -> bool:
        return all(self.map(pred))
    
    def flatten(self):
        return Chainable(chain.from_iterable(self))

    def flat_map(self, mapper: Callable[[T], Iterable[S]]) -> Chainable[S]:
        return self.map(mapper).flatten()
