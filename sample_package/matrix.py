"""This module defines a Matrix class."""

class Matrix:
    """A standard m-by-n-dimensional matrix from linear algebra.

    The class is designed for sub-classing in such a way that
    the user can adapt the typing class attribute to change,
    for example, how the entries are stored (e.g., as integers).

    Attributes:
        storage (callable): must return an iterable that is used
            to store the entries of the matrix; defaults to tuple
        typing (callable): type casting applied to all vector
            entries upon creation; defaults to float
        zero_threshold (float): maximum difference allowed when
            comparing an entry to zero; defaults to 1e-12
    """

    storage = tuple
    typing = float
    zero_threshold = 1e-12

    def __init__(self, data):
        """Initiate a new matrix.

        Args:
            data (iterable of iterables): the matrix's entries;
                must be provided with rows first, then column;
                the number of column entries must be consistent across rows
                where the first row sets the standard;
                must have at least one element in total

        Raises:
            ValueError:
                - if the number of columns is inconsistent across the rows
                - if the provided data do not have enough entries
        """
        self._entries = self.storage(
            self.storage(self.typing(x) for x in r) for r in data
        )
        for row in self._entries[1:]:
            if len(row) != self.n_cols:
                raise ValueError("each row must have the same number of entries")
        if len(self) == 0:
            raise ValueError("the matrix must have at least one entry")

    @classmethod
    def from_columns(cls, data):
        """Initiate a new matrix.

        This is an alternative constructor for data provided in column-major order.

        Args:
            data (iterable of iterables): the matrix's entries in column-major order;
                the number of column entries must be consistent per row
                while the first row sets the correct number;
                must have at least one element in total

        Raises:
            ValueError:
                - if the number of columns is inconsistent across the rows
                - if the provided data do not have enough entries
        """
        return cls(data).transpose()

    def __repr__(self):
        name = self.__class__.__name__
        args = ", ".join(
            "(" + ", ".join(f"{c:.3f}" for c in r) + ",)" for r in self._entries
        )
        return f"{name}(({args}))"

    def __str__(self):
        name = self.__class__.__name__
        first, last, m, n = self[0], self[-1], self.n_rows, self.n_cols
        return f"{name}(({first:.1f}, ...), ..., (..., {last:.1f}))[{m:d}x{n:d}]"

    @property
    def n_rows(self):
        """Number of rows in the matrix."""
        return len(self._entries)

    @property
    def n_cols(self):
        """Number of columns in the matrix."""
        return len(self._entries[0])

    def __len__(self):
        return self.n_rows * self.n_cols

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += len(self)
            if not (0 <= index < len(self)):
                raise IndexError("integer index out of range")
            row, col = divmod(index, self.n_cols)
            return self._entries[row][col]
        elif (
            isinstance(index, tuple)
            and len(index) == 2
            and isinstance(index[0], int)
            and isinstance(index[1], int)
        ):
            return self._entries[index[0]][index[1]]
        raise TypeError("index must be either an integer or a tuple of two integers")

    def rows(self):
        """Iterate over the rows of the matrix.

        Returns:
            rows (Generator): produces Vector instances
                representing individual rows of the matrix
        """
        return (Vector(r) for r in self._entries)

    def cols(self):
        """Iterate over the columns of the matrix.

        Returns:
            columns (Generator): produces Vector instances
                representing individual columns of the matrix
        """
        return (
            Vector(self._entries[r][c] for r in range(self.n_rows))
            for c in range(self.n_cols)
        )

    def entries(self, *, reverse=False, row_major=True):
        """Iterate over the entries of the matrix in flat fashion.

        Args:
            reverse (bool): flag to iterate backwards; defaults to False
            row_major (bool): flag to iterate in row major order; defaults to False

        Returns:
            entries (Generator): produces the entries rows of the matrix
                in the type set in the typing class variable
        """
        if reverse:
            rows, cols = range(self.n_rows - 1, -1, -1), range(self.n_cols - 1, -1, -1)
        else:
            rows, cols = range(self.n_rows), range(self.n_cols)
        if row_major:
            return (self._entries[r][c] for r in rows for c in cols)
        return (self._entries[r][c] for c in cols for r in rows)

    def __iter__(self):
        return self.entries()

    def __reversed__(self):
        return self.entries(reverse=True)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if (self.n_rows != other.n_rows) or (self.n_cols != other.n_cols):
                raise ValueError("matrices need to be of the same dimensions")
            return self.__class__(
                (s_col + o_col for (s_col, o_col) in zip(s_row, o_row))
                for (s_row, o_row) in zip(self._entries, other._entries)
            )
        elif isinstance(other, numbers.Number):
            return self.__class__((c + other for c in r) for r in self._entries)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Vector):
            raise TypeError("vectors and matrices cannot be added")
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        if isinstance(other, Vector):
            raise TypeError("vectors and matrices cannot be subtracted")
        return (-self) + other

    def _matrix_multiply(self, other):
        if self.n_cols != other.n_rows:
            raise ValueError("matrices need to have compatible dimensions")
        return self.__class__((rv * cv for cv in other.cols()) for rv in self.rows())

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return self.__class__((x * other for x in r) for r in self._entries)
        elif isinstance(other, Vector):
            return self._matrix_multiply(other.as_matrix()).as_vector()
        elif isinstance(other, self.__class__):
            return self._matrix_multiply(other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return self * other
        elif isinstance(other, Vector):
            return other.as_matrix(column=False)._matrix_multiply(self).as_vector()
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self * (1 / other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if (self.n_rows != other.n_rows) or (self.n_cols != other.n_cols):
                raise ValueError("matrices need to be of the same dimensions")
            for x, y in zip(self, other):
                if abs(x - y) > self.zero_threshold:
                    return False
            return True
        return NotImplemented

    def __pos__(self):
        return self

    def __neg__(self):
        return self.__class__((-x for x in r) for r in self._entries)

    def __abs__(self):
        return norm(self)

    def __bool__(self):
        return bool(abs(self))

    def __float__(self):
        if not (self.n_rows == 1 and self.n_cols == 1):
            raise RuntimeError("matrix must have exactly one entry to become a scalar")
        return self[0]

    def as_vector(self):
        """Cast the matrix as a one-dimensional vector.

        Returns:
            vector (Vector)

        Raises:
            RuntimeError: if not one of the two dimensions is 1
        """
        if not (self.n_rows == 1 or self.n_cols == 1):
            raise RuntimeError("one dimension (m or n) must be 1")
        return Vector(x for x in self)

    def transpose(self):
        """Transpose the rows and columns of the matrix.

        Returns:
            matrix (Matrix)
        """
        return self.__class__(zip(*self._entries))


from .vector import Vector
