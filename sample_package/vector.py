"""This module defines a Vector class."""

from .matrix import Matrix


class Vector:
    """A standard one-dimensional vector from linear algebra.

    The class is designed for sub-classing in such a way that
    the user can adapt the typing class attribute to change,
    for example, how the entries are stored (e.g., as integers).

    Attributes:
        storage (callable): must return an iterable that is used
            to store the entries of the vector; defaults to tuple
        typing (callable): type casting applied to all vector
            entries upon creation; defaults to float
        zero_threshold (float): maximum difference allowed when
            comparing an entry to zero; defaults to 1e-12
    """

    storage = tuple
    typing = float
    zero_threshold = 1e-12

    def __init__(self, data):
        """Initiate a new vector.

        Args:
            data (iterable): the vector's entries;
                must have at least one element

        Raises:
            ValueError: if the provided data do not have enough entries
        """
        self._entries = self.storage(self.typing(x) for x in data)
        if len(self) == 0:
            raise ValueError("the vector must have at least one entry")

    def __repr__(self):
        name, args = self.__class__.__name__, ", ".join(f"{x:.3f}" for x in self)
        return f"{name}(({args}))"

    def __str__(self):
        name, first, last, entries = (
            self.__class__.__name__,
            self[0],
            self[-1],
            len(self),
        )
        return f"{name}({first:.1f}, ..., {last:.1f})[{entries:d}]"

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        return self._entries[index]

    def __iter__(self):
        return iter(self._entries)

    def __reversed__(self):
        return reversed(self._entries)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors need to be of the same length")
            return self.__class__(x + y for (x, y) in zip(self, other))
        elif isinstance(other, numbers.Number):
            return self.__class__(x + other for x in self)
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors need to be of the same length")
            return sum(x * y for (x, y) in zip(self, other))
        elif isinstance(other, numbers.Number):
            return self.__class__(x * other for x in self)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self * (1 / other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors need to be of the same length")
            for x, y in zip(self, other):
                if abs(x - y) > self.zero_threshold:
                    return False
            return True
        return NotImplemented

    def __pos__(self):
        return self

    def __neg__(self):
        return self.__class__(-x for x in self)

    def __abs__(self):
        return norm(self)

    def __bool__(self):
        return bool(abs(self))

    def __float__(self):
        if len(self) != 1:
            raise RuntimeError("vector must have exactly one entry to become a scalar")
        return self[0]

    def as_matrix(self, *, column=True):
        """Convert the vector into a matrix.

        Args:
            column (bool): if the vector should be interpreted as
                as a column vector or not; defaults to True

        Returns:
            matrix (Matrix)
        """
        if column:
            return Matrix([x] for x in self)
        return Matrix([(x for x in self)])
