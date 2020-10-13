"""This is a sample module.

It defines three functions average(), average_evens(), and average_odds().
The point is to show how we can put Python code in a .py file to be re-used
in some other place.

We should never forget to document the code as well, both on the module
level (i.e., this docstring) but also in every function it defines.

When imported, Python modules are executed top to bottom before the flow of
execution returns to wherever they were imported into.

An important convention is to prefix variables and functions that are not to
be used outside the module with a single underscore "_". This way, we can
design the code within a module in a modular fashion and only "export" what we
want.

Here, all three functions internally forward parts of their computations
to the utility functions _round_all() and _scaled_average() that contain all
the logic common to the three functions.

While this example is stylized, it shows how Python modules are often
designed.
"""

def _round_all(numbers):
    """Internal utility function to round all numbers in a list."""
    return [round(n) for n in numbers]


def _scaled_average(numbers, scalar):
    """Internal utility function to calculate scaled averages."""
    average = sum(numbers) / len(numbers)
    return scalar * average


def average(numbers, *, scalar=1):
    """Calculate the average of all numbers in a list.

    Args:
        numbers (list of int's/float's): numbers to be averaged;
            if non-whole numbers are provided, they are rounded
        scalar (float, optional): multiplies the average; defaults to 1

    Returns:
        scaled_average (float)
    """
    return _scaled_average(_round_all(numbers), scalar)


def average_evens(numbers, *, scalar=1):
    """Calculate the average of all even numbers in a list.

    Args:
        numbers (list of int's/float's): numbers to be averaged;
            if non-whole numbers are provided, they are rounded
        scalar (float, optional): multiplies the average; defaults to 1

    Returns:
        scaled_average (float)
    """
    return _scaled_average([n for n in _round_all(numbers) if n % 2 == 0], scalar)


def average_odds(numbers, *, scalar=1):
    """Calculate the average of all odd numbers in a list.

    Args:
        numbers (list of int's/float's): numbers to be averaged;
            if non-whole numbers are provided, they are rounded
        scalar (float, optional): multiplies the average; defaults to 1

    Returns:
        scaled_average (float)
    """
    return _scaled_average([n for n in _round_all(numbers) if n % 2 != 0], scalar)
