# Base stage
FROM python:3.12-slim-bullseye as base

# Set working directory
WORKDIR /twich-lamoda-parser-fastapi

# Copy dependency files
COPY pyproject.toml poetry.lock /twich-lamoda-parser-fastapi/

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy application code
COPY app /twich-lamoda-parser-fastapi/

# FastAPI stage
FROM base as fastapi
RUN chmod +x entrypoints/entrypoint_fastapi.sh
CMD ["python", "main.py"]

FROM base as consumer
RUN chmod +x entrypoints/entrypoint_consumer.sh
CMD ["python", "start_consumer.py"]
