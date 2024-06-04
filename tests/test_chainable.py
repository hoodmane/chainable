from chainable import Chainable


def test_1():
    m = Chainable(range(5)).map(lambda x: x * x + 1)
    assert list(m) == [1, 2, 5, 10, 17]


def test_2():
    m = Chainable(range(15)).map(lambda x: x * x + 1).filter(lambda x: x % 3 == 1)
    assert list(m) == [1, 10, 37, 82, 145]


def test_flat_map():
    def proper_divisors(x):
        return (t for t in range(2, x) if x % t == 0)

    m = Chainable(range(6, 12 + 1)).flat_map(proper_divisors)
    assert list(m) == [2, 3, 2, 4, 3, 2, 5, 2, 3, 4, 6]


def test_lazy():
    predicate_calls = 0
    mapper_calls = 0

    def recording_predicate(x):
        nonlocal predicate_calls
        predicate_calls += 1
        return x % 3 == 1

    def recording_mapper(x):
        nonlocal mapper_calls
        mapper_calls += 1
        return (x - 1) // 3

    m = Chainable(range(6)).filter(recording_predicate).map(recording_mapper)
    it = iter(m)

    assert predicate_calls == 0
    assert mapper_calls == 0

    assert next(it) == 0
    assert predicate_calls == 2
    assert mapper_calls == 1

    assert next(it) == 1
    assert predicate_calls == 5
    assert mapper_calls == 2
