# Base stage
FROM python:3.12-slim-bullseye as base

# Set working directory
WORKDIR /parser

# Copy dependency files
COPY pyproject.toml poetry.lock .env /parser/

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY app /parser/

FROM base as fastapi
RUN chmod +x entrypoints/entrypoint_fastapi.sh
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
