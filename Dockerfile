# Python base image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Create a directory for the app
WORKDIR /app

# Add and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the application code
COPY . .

# Expose the port FastAPI runs on (default is 8000)
EXPOSE 8000

# Run Alembic migrations and then start the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn organization_manager.main:app --host localhost --port 8000"]