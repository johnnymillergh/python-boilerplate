# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

# Based on https://github.com/python-poetry/poetry/discussions/1879?sort=top#discussioncomment-216865
# Inpired by https://gist.github.com/usr-ein/c42d98abca3cb4632ab0c2c6aff8c88a
# but I try to keep it updated (see history)

################################
# PYTHON-BASE
# Sets up all our shared environment variables
################################
FROM python:3.13.7-slim AS python-base

# Setup env for Python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=2.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       # deps for installing poetry
       curl \
       # deps for building python deps
       build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

RUN poetry --version

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-interaction --no-root --without test

################################
# DEVELOPMENT
# Image used during development / testing
################################
FROM python-base AS development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /app

################################
# PRODUCTION
# Final image used for runtime
################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/
WORKDIR /app/src

RUN pwd
# Show the project module in the current directory. e.g.
# total 4.0K
# drwxr-xr-x 11 root root 4.0K Jan 1 12:59 python_boilerplate
RUN ls -lh

# Run the executable
ENTRYPOINT ["python", "-m", "python_boilerplate"]
CMD ["param_1_from_command_line", "param_2_from_command_line"]
