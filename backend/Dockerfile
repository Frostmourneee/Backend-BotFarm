FROM ghcr.io/astral-sh/uv:0.9.11-python3.13-alpine
WORKDIR /app
COPY pyproject.toml .
RUN ["uv", "sync"]
COPY . /app/backend
EXPOSE 8080
ENV PYTHONPATH=/app
CMD ["sh", "-c", "uv run alembic -c backend/db/alembic.ini upgrade head; uv run backend/scripts/create_admin_user.py; uv run -m backend"]