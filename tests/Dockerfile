FROM ghcr.io/astral-sh/uv:0.9.11-python3.13-alpine
WORKDIR /app
COPY backend/ ./backend/
COPY tests/ ./tests/
COPY backend/pyproject.toml .

RUN uv sync --group test
CMD ["uv", "run", "pytest", "tests", "-v", "--cov=backend", "--cov-report=html"]
