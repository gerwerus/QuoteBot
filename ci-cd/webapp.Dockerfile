FROM python:3.12-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.1

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY ./src/webapp/pyproject.toml .
COPY ./src/webapp/poetry.lock .
RUN . /venv/bin/activate && poetry install --no-root --no-dev

FROM base as final
COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"
COPY ./scripts/webapp-entrypoint.sh /scripts/webapp-entrypoint.sh
COPY ./src/webapp ./webapp

WORKDIR /app/webapp/

RUN chmod a+x /scripts/webapp-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/scripts/webapp-entrypoint.sh"]