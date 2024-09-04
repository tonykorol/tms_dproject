FROM python:3.12-alpine

WORKDIR /api_app

RUN pip install poetry --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-dev --no-interaction --no-ansi --no-cache

COPY . .

RUN chmod a+x docker_run/*.sh
