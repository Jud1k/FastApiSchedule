# Базовый образ
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --dev --all-extras

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH=/app

ENTRYPOINT []

CMD ["fastapi","run","--host","0.0.0.0","app/main.py"]