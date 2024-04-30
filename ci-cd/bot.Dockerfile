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

COPY pyproject.toml .
COPY poetry.lock .
RUN . /venv/bin/activate && poetry install

COPY ./src/bot .

FROM base as final
ENV PATH="/opt/venv/bin:$PATH"

COPY ./scripts/bot-entrypoint.sh /scripts/bot-entrypoint.sh
COPY ./src/bot .

RUN chmod a+x /scripts/docker-entrypoint.sh

CMD ["/scripts/docker-entrypoint.sh"]