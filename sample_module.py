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

Here, all three functions internally forward the computation to an internal
utility function _scaled_average() that contains all the logic common to the
three functions. Also, we define one _default_scalar variable that is used as
the default for the scalar parameter in each of the functions.

While this example is stylized, it shows how Python modules are often
designed.
"""

_default_scalar = 1


def _scaled_average(numbers, scalar):
    """Internal utility function to calculate scaled averages."""
    average = sum(numbers) / len(numbers)
    return scalar * average


def average(numbers, *, scalar=_default_scalar):
    """Calculate the average of all numbers in a list.

    Args:
        numbers (list): list of numbers; may be integers or floats
        scalar (float, optional): the scalar that multiplies the
            average of the even numbers

    Returns:
        float: (scaled) average
    """
    return _scaled_average(numbers, scalar)


def average_evens(numbers, *, scalar=_default_scalar):
    """Calculate the average of all even numbers in a list.

    Args:
        numbers (list): list of numbers; may be integers or floats
        scalar (float, optional): the scalar that multiplies the
            average of the even numbers

    Returns:
        float: (scaled) average
    """
    return _scaled_average([n for n in numbers if n % 2 == 0], scalar)


def average_odds(numbers, *, scalar=_default_scalar):
    """Calculate the average of all odd numbers in a list.

    Args:
        numbers (list): list of numbers; may be integers or floats
        scalar (float, optional): the scalar that multiplies the
            average of the even numbers

    Returns:
        float: (scaled) average
    """
    return _scaled_average([n for n in numbers if n % 2 != 0], scalar)
