"""Configure nox as the task runner."""

import nox


PYTHON = "3.8"

# Use a unified .cache/ folder for all develop tools.
nox.options.envdir = ".cache/nox"

# All tools except git and poetry are project dependencies.
# Avoid accidental successes if the environment is not set up properly.
nox.options.error_on_external_run = True
