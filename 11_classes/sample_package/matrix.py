"""This module defines a Matrix class."""

import numbers

# Note the import at the bottom of this file, and
# see the comments about imports in the matrix module.
from sample_package import utils


class Matrix:
    """An m-by-n-dimensional matrix from linear algebra.

    All entries are converted to floats, or whatever is set in the typing attribute.

    Attributes:
        storage (callable): data type used to store the entries internally;
            defaults to tuple
        typing (callable): type casting applied to all entries upon creation;
            defaults to float
        vector_cls (vector.Vector): a reference to the Vector class to work with
        zero_threshold (float): max. tolerance when comparing an entry to zero;
            defaults to 1e-12
    """

    storage = utils.DEFAULT_ENTRIES_STORAGE
    typing = utils.DEFAULT_ENTRY_TYPE
    # the `vector_cls` attribute is set at the bottom of this file
    zero_threshold = utils.ZERO_THRESHOLD

    def __init__(self, data):
        """Create a new matrix.

        Args:
            data (sequence of sequences): the matrix's entries;
                viewed as a sequence of the matrix's rows (i.e., row-major order);
                use the .from_columns() class method if the data come as a sequence
                of the matrix's columns (i.e., column-major order)

        Raises:
            ValueError:
                - if no entries are provided
                - if the number of columns is inconsistent across the rows

        Example Usage:
            >>> Matrix([(1, 2), (3, 4)])
            Matrix(((1.0, 2.0,), (3.0, 4.0,)))
        """
        self._entries = self.storage(
            self.storage(self.typing(x) for x in r) for r in data
        )
        for row in self._entries[1:]:
            if len(row) != self.n_cols:
                raise ValueError("rows must have the same number of entries")
        if len(self) == 0:
            raise ValueError("a matrix must have at least one entry")

    @classmethod
    def from_columns(cls, data):
        """Create a new matrix.

        This is an alternative constructor for data provided in column-major order.

        Args:
            data (sequence of sequences): the matrix's entries;
                viewed as a sequence of the matrix's columns (i.e., column-major order);
                use the normal constructor method if the data come as a sequence
                of the matrix's rows (i.e., row-major order)

        Raises:
            ValueError:
                - if no entries are provided
                - if the number of rows is inconsistent across the columns

        Example Usage:
            >>> Matrix.from_columns([(1, 2), (3, 4)])
            Matrix(((1.0, 3.0,), (2.0, 4.0,)))
        """
        return cls(data).transpose()

    @classmethod
    def from_rows(cls, data):
        """See docstring for .__init__()."""
        # Some users may want to use this .from_rows() constructor
        # to explicitly communicate that the data are in row-major order.
        # Otherwise, this method is redundant.
        return cls(data)

    def __repr__(self):
        """Text representation of a Matrix."""
        name = self.__class__.__name__
        args = ", ".join(
            "(" + ", ".join(repr(c) for c in r) + ",)" for r in self._entries
        )
        return f"{name}(({args}))"

    def __str__(self):
        """Human-readable text representation of a Matrix."""
        name = self.__class__.__name__
        first, last, m, n = self[0], self[-1], self.n_rows, self.n_cols
        return f"{name}(({first!r}, ...), ..., (..., {last!r}))[{m:d}x{n:d}]"

    @property
    def n_rows(self):
        """Number of rows in a Matrix."""
        return len(self._entries)

    @property
    def n_cols(self):
        """Number of columns in a Matrix."""
        return len(self._entries[0])

    def __len__(self):
        """Number of entries in a Matrix."""
        return self.n_rows * self.n_cols

    def __getitem__(self, index):
        """Obtain an individual entry of a Matrix.

        Args:
            index (int / tuple of int's): if index is an integer,
                the Matrix is viewed as a sequence in row-major order;
                if index is a tuple of integers, the first one refers to
                the row and the second one to the column of the entry

        Returns:
            entry (Matrix.typing)

        Example Usage:
            >>> m = Matrix([(1, 2), (3, 4)])
            >>> m[0]
            1.0
            >>> m[-1]
            4.0
            >>> m[0, 1]
            2.0
        """
        # Sequence-like indexing (one-dimensional)
        if isinstance(index, int):
            if index < 0:
                index += len(self)
            if not (0 <= index < len(self)):
                raise IndexError("integer index out of range")
            row, col = divmod(index, self.n_cols)
            return self._entries[row][col]
        # Mathematical-like indexing (two-dimensional)
        elif (
            isinstance(index, tuple)
            and len(index) == 2
            and isinstance(index[0], int)
            and isinstance(index[1], int)
        ):
            return self._entries[index[0]][index[1]]
        raise TypeError("index must be either an int or a tuple of two int's")

    def rows(self):
        """Loop over a Matrix's rows.

        Returns:
            rows (generator): produces a Matrix's rows as Vectors
        """
        return (self.vector_cls(r) for r in self._entries)

    def cols(self):
        """Loop over a Matrix's columns.

        Returns:
            columns (generator): produces a Matrix's columns as Vectors
        """
        return (
            self.vector_cls(self._entries[r][c] for r in range(self.n_rows))
            for c in range(self.n_cols)
        )

    def entries(self, *, reverse=False, row_major=True):
        """Loop over a Matrix's entries.

        Args:
            reverse (bool): flag to loop backwards; defaults to False
            row_major (bool): flag to loop in row-major order; defaults to True

        Returns:
            entries (generator): produces a Matrix's entries
        """
        if reverse:
            rows = range(self.n_rows - 1, -1, -1)
            cols = range(self.n_cols - 1, -1, -1)
        else:
            rows, cols = range(self.n_rows), range(self.n_cols)
        if row_major:
            return (self._entries[r][c] for r in rows for c in cols)
        return (self._entries[r][c] for c in cols for r in rows)

    def __iter__(self):
        """Loop over a Matrix's entries.

        See .entries() for more customization options.
        """
        return self.entries()

    def __reversed__(self):
        """Loop over a Matrix's entries in reverse order.

        See .entries() for more customization options.
        """
        return self.entries(reverse=True)

    def __add__(self, other):
        """Handle `self + other` and `other + self`.

        This may be either matrix addition or broadcasting addition.

        Example Usage:
            >>> Matrix([(1, 2), (3, 4)]) + Matrix([(2, 3), (4, 5)])
            Matrix(((3.0, 5.0,), (7.0, 9.0,)))

            >>> Matrix([(1, 2), (3, 4)]) + 5
            Matrix(((6.0, 7.0,), (8.0, 9.0,)))

            >>> 10 + Matrix([(1, 2), (3, 4)])
            Matrix(((11.0, 12.0,), (13.0, 14.0,)))
        """
        # Matrix addition
        if isinstance(other, self.__class__):
            if (self.n_rows != other.n_rows) or (self.n_cols != other.n_cols):
                raise ValueError("matrices must have the same dimensions")
            return self.__class__(
                (s_col + o_col for (s_col, o_col) in zip(s_row, o_row))
                for (s_row, o_row) in zip(self._entries, other._entries)
            )
        # Broadcasting addition
        elif isinstance(other, numbers.Number):
            return self.__class__((c + other for c in r) for r in self._entries)
        return NotImplemented

    def __radd__(self, other):
        """See docstring for .__add__()."""
        if isinstance(other, self.vector_cls):
            raise TypeError("vectors and matrices cannot be added")
        # As both matrix and broadcasting addition are commutative,
        # we dispatch to .__add__().
        return self + other

    def __sub__(self, other):
        """Handle `self - other` and `other - self`.

        This may be either matrix subtraction or broadcasting subtraction.

        Example Usage:
            >>> Matrix([(2, 3), (4, 5)]) - Matrix([(1, 2), (3, 4)])
            Matrix(((1.0, 1.0,), (1.0, 1.0,)))

            >>> Matrix([(1, 2), (3, 4)]) - 1
            Matrix(((0.0, 1.0,), (2.0, 3.0,)))

            >>> 10 - Matrix([(1, 2), (3, 4)])
            Matrix(((9.0, 8.0,), (7.0, 6.0,)))
        """
        # As subtraction is the inverse of addition,
        # we first dispatch to .__neg__() to invert the signs of
        # all entries in other and then dispatch to .__add__().
        return self + (-other)

    def __rsub__(self, other):
        """See docstring for .__sub__()."""
        if isinstance(other, self.vector_cls):
            raise TypeError("vectors and matrices cannot be subtracted")
        # Same comments as in .__sub__() apply
        # with the roles of self and other swapped.
        return (-self) + other

    def _matrix_multiply(self, other):
        """Internal utility method to multiply to Matrix instances."""
        if self.n_cols != other.n_rows:
            raise ValueError("matrices must have compatible dimensions")
        # Matrix-matrix multiplication means that each entry of the resulting
        # Matrix is the dot product of the respective row of the "left" Matrix
        # and column of the "right" Matrix. So, the rows/columns are represented
        # by the Vector instances provided by the .cols() and .rows() methods.
        return self.__class__((rv * cv for cv in other.cols()) for rv in self.rows())

    def __mul__(self, other):
        """Handle `self * other` and `other * self`.

        This may be either scalar multiplication, matrix-vector multiplication,
        vector-matrix multiplication, or matrix-matrix multiplication.

        Example Usage:
            >>> Matrix([(1, 2), (3, 4)]) * Matrix([(1, 2), (3, 4)])
            Matrix(((7.0, 10.0,), (15.0, 22.0,)))

            >>> 2 * Matrix([(1, 2), (3, 4)])
            Matrix(((2.0, 4.0,), (6.0, 8.0,)))

            >>> Matrix([(1, 2), (3, 4)]) * 3
            Matrix(((3.0, 6.0,), (9.0, 12.0,)))

            Matrix-vector and vector-matrix multiplication are not commutative.

            >>> from sample_package import Vector

            >>> Matrix([(1, 2), (3, 4)]) * Vector([5, 6])
            Vector((17.0, 39.0))

            >>> Vector([5, 6]) * Matrix([(1, 2), (3, 4)])
            Vector((23.0, 34.0))
        """
        # Scalar multiplication
        if isinstance(other, numbers.Number):
            return self.__class__((x * other for x in r) for r in self._entries)
        # Matrix-vector multiplication: Vector is a column Vector
        elif isinstance(other, self.vector_cls):
            # First, cast the other Vector as a Matrix, then do matrix-matrix
            # multiplication, and lastly return the result as a Vector again.
            return self._matrix_multiply(other.as_matrix()).as_vector()
        # Matrix-matrix multiplication
        elif isinstance(other, self.__class__):
            return self._matrix_multiply(other)
        return NotImplemented

    def __rmul__(self, other):
        """See docstring for .__mul__()."""
        # As scalar multiplication is commutative, we dispatch to .__mul__().
        if isinstance(other, numbers.Number):
            return self * other
        # Vector-matrix multiplication: Vector is a row Vector
        elif isinstance(other, self.vector_cls):
            return other.as_matrix(column=False)._matrix_multiply(self).as_vector()
        return NotImplemented

    def __truediv__(self, other):
        """Handle `self / other`.

        Divide a Matrix by a scalar.

        Example Usage:
            >>> Matrix([(1, 2), (3, 4)]) / 4
            Matrix(((0.25, 0.5,), (0.75, 1.0,)))
        """
        # As scalar division division is the same as multiplication
        # with the inverse, we dispatch to .__mul__().
        if isinstance(other, numbers.Number):
            return self * (1 / other)
        return NotImplemented

    def __eq__(self, other):
        """Handle `self == other`.

        Compare two Matrix instances for equality.

        Example Usage:
            >>> Matrix([(1, 2), (3, 4)]) == Matrix([(1, 2), (3, 4)])
            True

            >>> Matrix([(1, 2), (3, 4)]) == Matrix([(5, 6), (7, 8)])
            False
        """
        if isinstance(other, self.__class__):
            if (self.n_rows != other.n_rows) or (self.n_cols != other.n_cols):
                raise ValueError("matrices must have the same dimensions")
            for x, y in zip(self, other):
                if abs(x - y) > self.zero_threshold:
                    return False  # exit early if two corresponding entries differ
            return True
        return NotImplemented

    def __pos__(self):
        """Handle `+self`.

        This is simply an identity operator returning the Matrix itself.
        """
        return self

    def __neg__(self):
        """Handle `-self`.

        Negate all entries of a Matrix.
        """
        return self.__class__((-x for x in r) for r in self._entries)

    def __abs__(self):
        """The Frobenius norm of a Matrix."""
        return utils.norm(self)  # uses the norm() function shared vector.Vector

    def __bool__(self):
        """A Matrix is truthy if its Frobenius norm is strictly positive."""
        return bool(abs(self))

    def __float__(self):
        """Cast a Matrix as a scalar.

        Returns:
            scalar (float)

        Raises:
            RuntimeError: if the Matrix has more than one entry
        """
        if not (self.n_rows == 1 and self.n_cols == 1):
            raise RuntimeError("matrix must have exactly one entry to become a scalar")
        return self[0]

    def as_vector(self):
        """Get a Vector representation of a Matrix.

        Returns:
            vector (vector.Vector)

        Raises:
            RuntimeError: if one of the two dimensions, .n_rows or .n_cols, is not 1

        Example Usage:
            >>> Matrix([(1, 2, 3)]).as_vector()
            Vector((1.0, 2.0, 3.0))
        """
        if not (self.n_rows == 1 or self.n_cols == 1):
            raise RuntimeError("one dimension (m or n) must be 1")
        return self.vector_cls(x for x in self)

    def transpose(self):
        """Switch the rows and columns of a Matrix.

        Returns:
            matrix (Matrix)

        Example Usage:
            >>> m = Matrix([(1, 2), (3, 4)])
            >>> m
            Matrix(((1.0, 2.0,), (3.0, 4.0,)))
            >>> m.transpose()
            Matrix(((1.0, 3.0,), (2.0, 4.0,)))
        """
        return self.__class__(zip(*self._entries))


# This import needs to be made here as otherwise an ImportError is raised.
# That is so as both the matrix and vector modules import a class from each other.
# We call that a circular import. Whereas Python handles "circular" references
# (e.g., both the Matrix and Vector classes have methods that reference the
# respective other class), that is forbidden for imports.
from sample_package import vector

# This attribute cannot be set in the class definition
# as the vector module is only imported down here.
Matrix.vector_cls = vector.Vector
