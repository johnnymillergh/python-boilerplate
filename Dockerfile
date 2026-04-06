# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

# https://docs.roxautomation.com/linux/docker_best_practices/#multi-stage-build-patterns-with-uv

FROM python:3.14.3-slim AS base

# Build stage
FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first (optimal caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy and install application
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage
FROM base
RUN groupadd -r app && useradd -r -d /app -g app app
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
USER app
WORKDIR /app/src

# Run the executable
ENTRYPOINT ["python", "-m", "python_boilerplate"]
CMD ["param_1_from_command_line", "param_2_from_command_line"]
