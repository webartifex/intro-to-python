"""This module provides utility functions."""


def norm(vector_or_matrix):
    """Calculate the Frobenius or Euclidean norm of a matrix or vector.

    Args:
        vector_or_matrix (Vector/Matrix): the entries whose squares
            are to be summed up

    Returns:
        norm (float)
    """
    return math.sqrt(sum(x ** 2 for x in vector_or_matrix))
