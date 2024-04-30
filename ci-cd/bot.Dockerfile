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

COPY pyproject.toml .
COPY poetry.lock .
RUN . /venv/bin/activate && poetry install --no-root

FROM base as final
COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"
COPY ./scripts/bot-entrypoint.sh /scripts/bot-entrypoint.sh
COPY ./src/bot ./bot

RUN chmod a+x /scripts/bot-entrypoint.sh

CMD ["/scripts/bot-entrypoint.sh"]