FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        make \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md Dockerfile .dockerignore ./
COPY .github ./.github
COPY src ./src
COPY tests ./tests
COPY dbt ./dbt
COPY docs ./docs
COPY dashboard ./dashboard
COPY orchestration ./orchestration
COPY Makefile ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e ".[dev]"

CMD ["make", "check"]
