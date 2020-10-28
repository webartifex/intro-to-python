"""Configure nox as the task runner.

Nox provides the following tasks:

- "init-project": install the pre-commit hooks

- "doctests": run the xdoctests in the source files

- "fix-branch-references": adjusts links with git branch references in
  various files (e.g., Mardown or notebooks)

"""

import contextlib
import glob
import os
import re
import shutil
import subprocess
import tempfile

import nox


REPOSITORY = "webartifex/intro-to-python"

SRC_LOCATIONS = (
    "02_functions/sample_module.py",
    "11_classes/sample_package",
)

# Use a unified .cache/ folder for all develop tools.
nox.options.envdir = ".cache/nox"

# All tools except git and poetry are project dependencies.
# Avoid accidental successes if the environment is not set up properly.
nox.options.error_on_external_run = True


@nox.session(name="init-project", venv_backend="none")
def init_project(session):
    """Install the pre-commit hooks."""
    for type_ in (
        "pre-commit",
        "pre-merge-commit",
    ):
        session.run("poetry", "run", "pre-commit", "install", f"--hook-type={type_}")

    # Copy the extensions' JavaScript and CSS files into Jupyter's search directory.
    session.run(
        "poetry", "run", "jupyter", "contrib", "nbextension", "install", "--user"
    )


@nox.session(venv_backend="none")
def doctests(session):
    """Run the xdoctests in the source files."""
    for location in SRC_LOCATIONS:
        session.run("poetry", "run", "xdoctest", "--silent", location)


@nox.session(name="fix-branch-references", venv_backend="none")
def fix_branch_references(_session):
    """Change git branch references.

    Intended to be run as a pre-commit hook.

    Many files in the project (e.g., README.md) contain links to resources on
    github.com, nbviewer.jupyter.org, or mybinder.org that contain git branch
    labels.

    This task rewrites branch labels into either "main" or "develop".
    """
    # Glob patterns that expand into the files whose links are re-written.
    paths = ["*.md", "**/*.ipynb"]

    branch = (
        subprocess.check_output(
            ("git", "rev-parse", "--abbrev-ref", "HEAD"),
        )
        .decode()
        .strip()
    )
    # If the current branch is only temporary and will be merged into "main", ...
    if branch.startswith("release-") or branch.startswith("hotfix-"):
        branch = "main"
    # If the branch is not "main", we assume it is a feature branch.
    elif branch != "main":
        branch = "develop"

    rewrites = [
        {
            "name": "github",
            "pattern": re.compile(
                fr"((((http)|(https))://github\.com/{REPOSITORY}/((blob)|(tree))/)([\w-]+)/)"
            ),
            "replacement": fr"\2{branch}/",
        },
        {
            "name": "nbviewer",
            "pattern": re.compile(
                fr"((((http)|(https))://nbviewer\.jupyter\.org/github/{REPOSITORY}/((blob)|(tree))/)([\w-]+)/)",
            ),
            "replacement": fr"\2{branch}/",
        },
        {
            "name": "mybinder",
            "pattern": re.compile(
                fr"((((http)|(https))://mybinder\.org/v2/gh/{REPOSITORY}/)([\w-]+)\?)",
            ),
            "replacement": fr"\2{branch}?",
        },
    ]

    for expanded in _expand(*paths):
        with _line_by_line_replace(expanded) as (old_file, new_file):
            for line in old_file:
                for rewrite in rewrites:
                    line = re.sub(rewrite["pattern"], rewrite["replacement"], line)
                new_file.write(line)


def _expand(*patterns):
    """Expand glob patterns into paths.

    Args:
        *patterns: the patterns to be expanded

    Yields:
        path: a single expanded path
    """
    for pattern in patterns:
        yield from glob.glob(pattern.strip())


@contextlib.contextmanager
def _line_by_line_replace(path):
    """Replace/change the lines in a file one by one.

    This generator function yields two file handles, one to the current file
    (i.e., `old_file`) and one to its replacement (i.e., `new_file`).

    Usage: loop over the lines in `old_file` and write the files to be kept
    to `new_file`. Files not written to `new_file` are removed!

    Args:
        path: the file whose lines are to be replaced

    Yields:
        old_file, new_file: handles to a file and its replacement
    """
    file_handle, new_file_path = tempfile.mkstemp()
    with os.fdopen(file_handle, "w") as new_file:
        with open(path) as old_file:
            yield old_file, new_file

    shutil.copymode(path, new_file_path)
    os.remove(path)
    shutil.move(new_file_path, path)
