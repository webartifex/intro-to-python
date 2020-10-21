"""Simulation of random streams of data.

This module defines:
- a generator object `data` modeling an infinite stream of integers
- a function `make_finite_stream()` that creates finite streams of data

The probability distribution underlying the integers is Gaussian-like with a
mean of 42 and a standard deviation of 8. The left tail of the distribution is
cut off meaning that the streams only produce non-negative numbers. Further,
one in a hundred random numbers has an increased chance to be an outlier.
"""

import itertools as _itertools
import random as _random


_random.seed(87)


def _infinite_stream():
    """Internal generator function to simulate an infinite stream of data."""
    while True:
        number = max(0, int(_random.gauss(42, 8)))
        if _random.randint(1, 100) == 1:
            number *= 2
        yield number


def make_finite_stream(min_=5, max_=15):
    """Simulate a finite stream of data.

    The returned stream is finite, but the number of elements to be produced
    by it is still random. This default behavior may be turned off by passing
    in `min_` and `max_` arguments with `min_ == max_`.

    Args:
        min_ (optional, int): minimum numbers in the stream; defaults to 5
        max_ (optional, int): maximum numbers in the stream; defaults to 15

    Returns:
        finite_stream (generator)

    Raises:
        ValueError: if max_ < min_
    """
    stream = _infinite_stream()
    n = _random.randint(min_, max_)
    yield from _itertools.islice(stream, n)


data = _infinite_stream()
