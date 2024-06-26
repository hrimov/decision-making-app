FROM python:3.11 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update \
 && apt-get install -y gcc git libpq-dev

WORKDIR $PYSETUP_PATH

# due to the installation of the project itself, it should contain all the files
COPY . .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir poetry

RUN poetry install --only main

FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR decision-making-app/

COPY . /decision-making-app/

CMD ["python", "-Om", "dma"]
