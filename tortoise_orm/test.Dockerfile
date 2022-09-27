FROM python:3.8.5

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python -m pip --no-cache-dir install --upgrade pip
RUN python -m pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.path /virtualenv && \
    poetry config virtualenvs.in-project false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY pytest.ini app ./
