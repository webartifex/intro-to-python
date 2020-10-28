"""This package provides linear algebra functionalities.

The package is split into three modules:
- matrix: defines the Matrix class
- vector: defines the Vector class
- utils: defines the norm() function that is shared by Matrix and Vector
         and package-wide constants

The classes implement arithmetic operations involving vectors and matrices.

See the docstrings in the modules and classes for further info.
"""

# Import the classes here so that they are available
# from the package's top level. That means that a user
# who imports this package with `import sample_package`
# may then refer to, for example, the Matrix class with
# simply `sample_package.Matrix` instead of the longer
# `sample_package.matrix.Matrix`.
from sample_package.matrix import Matrix
from sample_package.vector import Vector


# Define meta information for the package.
# There are other (and more modern) ways of
# doing this, but specifying the following
# dunder variables here is the traditional way.
__name__ = "linear_algebra_tools"
__version__ = "0.1.0"  # see https://semver.org/ for how the format works
__author__ = "Alexander Hess"

# Define what is imported with the "star import"
# (i.e., with `from sample_package import *`).
__all__ = ["Matrix", "Vector"]
