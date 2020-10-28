"""This module provides utilities for the whole package.

The defined constants are used as defaults in the Vector and Matrix classes.

The norm() function is shared by Vector.__abs__() and Matrix.__abs__().
"""

import math


# Define constants (i.e., normal variables that are, by convention, named in UPPERCASE)
# that are used as the defaults for class attributes within Vector and Matrix.
DEFAULT_ENTRIES_STORAGE = tuple
DEFAULT_ENTRY_TYPE = float
ZERO_THRESHOLD = 1e-12


def norm(vec_or_mat):
    """Calculate the Frobenius or Euclidean norm of a matrix or vector.

    Find more infos here: https://en.wikipedia.org/wiki/Matrix_norm#Frobenius_norm

    Args:
        vec_or_mat (Vector / Matrix): object whose entries are squared and summed up

    Returns:
        norm (float)

    Example Usage:
        As Vector and Matrix objects are by design non-empty sequences,
        norm() may be called, for example, with `[3, 4]` as the argument:
        >>> norm([3, 4])
        5.0
    """
    return math.sqrt(sum(x ** 2 for x in vec_or_mat))
