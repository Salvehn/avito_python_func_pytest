from typing import Iterable, List, Callable, Iterator, Union
import doctest
import pytest

def ilen(iterable: Iterable):
    """
    >>> foo = (x for x in range(10))
    >>> ilen(foo)
    10
    """
    return sum(1 for e in iterable)


@pytest.mark.parametrize('value,expected', [
    ((x for x in range(10)), 10),
    ({'1': 'a', '2': 'b'}, 2),
    (set('12345'), 5),
    ([1, 2, 3, 4, 5], 5),
    ((1, 2, 3, 4, 5), 5),
    (range(0), 0)
])
def test_ilen(value: Iterable, expected: int) -> None:
    """
    ilen test with various data types (generator, dict, set, list, tuple).
    """
    assert ilen(value) == expected


def flatten(iterable: Iterable):
    for obj in iterable:
        # если подобъект итерируемый и не строка - рекурсировать, иначе вернуть его
        if isinstance(obj, Iterable) and not isinstance(obj, str):
            for subiterable in flatten(obj):
                yield subiterable
        else:
            yield obj


@pytest.mark.parametrize('value,expected', [
    ([0, [1, [2, 3]]], [0, 1, 2, 3]),
    (['ab', ['cd', ['ef', 'gh']]], ['ab', 'cd', 'ef', 'gh'])
])
def test_flatten(value: Iterable, expected: Iterable) -> None:
    """
    Flatten test
    """
    assert list(flatten(value)) == expected


def distinct(iterable: Iterable):
    """
    >>> list(distinct([1, 2, 0, 1, 3, 0, 2]))
    [1, 2, 0, 3]
    """
    return list(dict.fromkeys(iterable))

@pytest.mark.parametrize('value,expected', [
    ([1, 2, 0, 1, 3, 0, 2], [1, 2, 0, 3]),
    (['Car', 'Boat', 'Plane', 'Car'], ['Car', 'Boat', 'Plane'])
])
def test_distinct(value: Iterable, expected: Iterable) -> None:
    """
    Distinct test.
    """
    assert list(distinct(value)) == expected




def groupby(key, iterable: Iterable):
    """
    >>> users = [
        {'gender': 'female', 'age': 33},
        {'gender': 'male', 'age': 20},
        {'gender': 'female', 'age': 21},
    ]
    >>> groupby('gender', users)
    {
        'female': [
            {'gender': 'female', 'age': 23},
            {'gender': 'female', 'age': 21},
        ],
        'male': [{'gender': 'male', 'age': 20}],
    }
    # Или так:
    >>> groupby('age', users)
    """
    d = {}
    for item in iterable:
        d.setdefault(item[key], []).append(item)
    return d

def test_groupby_gender() -> None:
    """
    assuming gender test
    """
    users = [
        {'gender': 'female', 'age': 33},
        {'gender': 'male', 'age': 20},
        {'gender': 'female', 'age': 21},
    ]
    result = {
        'female': [
            {'gender': 'female', 'age': 33},
            {'gender': 'female', 'age': 21},
        ],
        'male': [{'gender': 'male', 'age': 20}]
    }

    assert groupby('gender', users) == result


##test failed - result = [(0, 1, 2), (3, 4)] instead of [(0, 1, 2), (3, 4, )]
def chunks_v01(size: int, iterable: Iterable):
    """
    >>> list(chunks(3, [0, 1, 2, 3, 4]))
    [(0, 1, 2), (3, 4, )]
    """
    return [tuple(iterable[i:i+size]) for i in range(0, len(iterable), size)]


def chunks(size: int, iterable: Iterable):
    packet = []
    for n in range(size):
        packet.append(None)
    n = 0
    for obj in iterable:
        packet[n] = obj
        if n == size-1:
            n = 0
            yield tuple(packet)
        else:
            n += 1
    while n < size:
        packet[n] = None
        n += 1
    yield tuple(packet)


@pytest.mark.parametrize('size,value,expected', [
    (3, [0, 1, 2, 3, 4], [(0, 1, 2), (3, 4, None)]),
    (4, (x for x in range(5)),
     [(0, 1, 2, 3), (4, None, None, None)])
])
def test_chunks(size: int, value: Iterable, expected: Iterable) -> None:
    """
    Тестирование функции chunks
    """
    assert list(chunks(size, value)) == expected



def first(iterable: Iterable):
    """
    >>> foo = (x for x in range(10))
    >>> first(foo)
    0
    >>> first(range(0))
    None
    """
    try:
        return next(iter(iterable), None)
    except StopIteration:
        return None


@pytest.mark.parametrize('value,expected', [
    ((x for x in range(10)), 0),
    (range(0), None)
])
def test_first(value: Iterable, expected) -> None:
    """
    first() test
    """
    assert first(value) == expected

def test_first_complete() -> None:
    """
    Тестирование first на stopIteration
    (нет следующего элемента во время итерирования объекта с лишь одним значением)
    """
    temp = (x for x in range(1))
    first(temp)
    assert first(temp) is None

#test failed result - range(5) on 4th iter assert 4 == None, expected None
def last_v01(iterable: Iterable):
    """
    >>> foo = (x for x in range(10))
    >>> last(foo)
    9
    >>> last(range(0))
    None
    """
    item = None
    for item in iterable:
        pass
    return item

def last(iterable: Iterable):
        try:
            base_obj = next(iterable)
            for obj in iterable:
                base_obj = obj
        except TypeError:
            return None
        except StopIteration:
            return None
        else:
            return base_obj

@pytest.mark.parametrize('value,expected', [
    ((x for x in range(10)), 9),
    (range(0), None),
    (range(5), None)
])
def test_last(value: Iterable, expected) -> None:
    """
    Тестирование last
    """
    assert last(value) == expected


if __name__ == "__main__":
    doctest.testmod()
