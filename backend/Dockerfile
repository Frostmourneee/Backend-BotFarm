FROM ghcr.io/astral-sh/uv:0.9.11-python3.13-alpine
WORKDIR /app
COPY pyproject.toml .
RUN ["uv", "sync"]
COPY . /app/backend
EXPOSE 8080
CMD ["uv", "run", "-m", "backend"]
