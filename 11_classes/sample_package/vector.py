"""This module defines a Vector class."""

# Imports from the standard library go first ...
import numbers

# ... and are followed by project-internal ones.
# If third-party libraries are needed, they are
# put into a group on their own in between.
# Within a group, imports are sorted lexicographically.
from sample_package import matrix
from sample_package import utils


class Vector:
    """A one-dimensional vector from linear algebra.

    All entries are converted to floats, or whatever is set in the typing attribute.

    Attributes:
        matrix_cls (matrix.Matrix): a reference to the Matrix class to work with
        storage (callable): data type used to store the entries internally;
            defaults to tuple
        typing (callable): type casting applied to all entries upon creation;
            defaults to float
        zero_threshold (float): max. tolerance when comparing an entry to zero;
            defaults to 1e-12
    """

    matrix_cls = matrix.Matrix
    storage = utils.DEFAULT_ENTRIES_STORAGE
    typing = utils.DEFAULT_ENTRY_TYPE
    zero_threshold = utils.ZERO_THRESHOLD

    def __init__(self, data):
        """Create a new vector.

        Args:
            data (sequence): the vector's entries

        Raises:
            ValueError: if no entries are provided

        Example Usage:
            >>> Vector([1, 2, 3])
            Vector((1.0, 2.0, 3.0))

            >>> Vector(range(3))
            Vector((0.0, 1.0, 2.0))
        """
        self._entries = self.storage(self.typing(x) for x in data)
        if len(self) == 0:
            raise ValueError("a vector must have at least one entry")

    def __repr__(self):
        """Text representation of a Vector."""
        name = self.__class__.__name__
        args = ", ".join(repr(x) for x in self)
        return f"{name}(({args}))"

    def __str__(self):
        """Human-readable text representation of a Vector."""
        name = self.__class__.__name__
        first, last, n_entries = self[0], self[-1], len(self)
        return f"{name}({first!r}, ..., {last!r})[{n_entries:d}]"

    def __len__(self):
        """Number of entries in a Vector."""
        return len(self._entries)

    def __getitem__(self, index):
        """Obtain an individual entry of a Vector."""
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        return self._entries[index]

    def __iter__(self):
        """Loop over a Vector's entries."""
        return iter(self._entries)

    def __reversed__(self):
        """Loop over a Vector's entries in reverse order."""
        return reversed(self._entries)

    def __add__(self, other):
        """Handle `self + other` and `other + self`.

        This may be either vector addition or broadcasting addition.

        Example Usage:
            >>> Vector([1, 2, 3]) + Vector([2, 3, 4])
            Vector((3.0, 5.0, 7.0))

            >>> Vector([1, 2, 3]) + 4
            Vector((5.0, 6.0, 7.0))

            >>> 10 + Vector([1, 2, 3])
            Vector((11.0, 12.0, 13.0))
        """
        # Vector addition
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors must be of the same length")
            return self.__class__(x + y for (x, y) in zip(self, other))
        # Broadcasting addition
        elif isinstance(other, numbers.Number):
            return self.__class__(x + other for x in self)
        return NotImplemented

    def __radd__(self, other):
        """See docstring for .__add__()."""
        # As both vector and broadcasting addition are commutative,
        # we dispatch to .__add__().
        return self + other

    def __sub__(self, other):
        """Handle `self - other` and `other - self`.

        This may be either vector subtraction or broadcasting subtraction.

        Example Usage:
            >>> Vector([7, 8, 9]) - Vector([1, 2, 3])
            Vector((6.0, 6.0, 6.0))

            >>> Vector([1, 2, 3]) - 1
            Vector((0.0, 1.0, 2.0))

            >>> 10 - Vector([1, 2, 3])
            Vector((9.0, 8.0, 7.0))
        """
        # As subtraction is the inverse of addition,
        # we first dispatch to .__neg__() to invert the signs of
        # all entries in other and then dispatch to .__add__().
        return self + (-other)

    def __rsub__(self, other):
        """See docstring for .__sub__()."""
        # Same comments as in .__sub__() apply
        # with the roles of self and other swapped.
        return (-self) + other

    def __mul__(self, other):
        """Handle `self * other` and `other * self`.

        This may be either the dot product of two vectors or scalar multiplication.

        Example Usage:
            >>> Vector([1, 2, 3]) * Vector([2, 3, 4])
            20.0

            >>> 2 * Vector([1, 2, 3])
            Vector((2.0, 4.0, 6.0))

            >>> Vector([1, 2, 3]) * 3
            Vector((3.0, 6.0, 9.0))
        """
        # Dot product
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors must be of the same length")
            return sum(x * y for (x, y) in zip(self, other))
        # Scalar multiplication
        elif isinstance(other, numbers.Number):
            return self.__class__(x * other for x in self)
        return NotImplemented

    def __rmul__(self, other):
        """See docstring for .__mul__()."""
        # As both dot product and scalar multiplication are commutative,
        # we dispatch to .__mul__().
        return self * other

    def __truediv__(self, other):
        """Handle `self / other`.

        Divide a Vector by a scalar.

        Example Usage:
            >>> Vector([9, 6, 12]) / 3
            Vector((3.0, 2.0, 4.0))
        """
        # As scalar division division is the same as multiplication
        # with the inverse, we dispatch to .__mul__().
        if isinstance(other, numbers.Number):
            return self * (1 / other)
        return NotImplemented

    def __eq__(self, other):
        """Handle `self == other`.

        Compare two Vectors for equality.

        Example Usage:
            >>> Vector([1, 2, 3]) == Vector([1, 2, 3])
            True

            >>> Vector([1, 2, 3]) == Vector([4, 5, 6])
            False
        """
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                raise ValueError("vectors must be of the same length")
            for x, y in zip(self, other):
                if abs(x - y) > self.zero_threshold:
                    return False  # exit early if two corresponding entries differ
            return True
        return NotImplemented

    def __pos__(self):
        """Handle `+self`.

        This is simply an identity operator returning the Vector itself.
        """
        return self

    def __neg__(self):
        """Handle `-self`.

        Negate all entries of a Vector.
        """
        return self.__class__(-x for x in self)

    def __abs__(self):
        """The Euclidean norm of a vector."""
        return utils.norm(self)  # uses the norm() function shared matrix.Matrix

    def __bool__(self):
        """A Vector is truthy if its Euclidean norm is strictly positive."""
        return bool(abs(self))

    def __float__(self):
        """Cast a Vector as a scalar.

        Returns:
            scalar (float)

        Raises:
            RuntimeError: if the Vector has more than one entry
        """
        if len(self) != 1:
            raise RuntimeError("vector must have exactly one entry to become a scalar")
        return self[0]

    def as_matrix(self, *, column=True):
        """Get a Matrix representation of a Vector.

        Args:
            column (bool): if the vector is interpreted as a
                column vector or a row vector; defaults to True

        Returns:
            matrix (matrix.Matrix)

        Example Usage:
            >>> v = Vector([1, 2, 3])
            >>> v.as_matrix()
            Matrix(((1.0,), (2.0,), (3.0,)))
            >>> v.as_matrix(column=False)
            Matrix(((1.0, 2.0, 3.0,)))
        """
        if column:
            return self.matrix_cls([x] for x in self)
        return self.matrix_cls([(x for x in self)])
