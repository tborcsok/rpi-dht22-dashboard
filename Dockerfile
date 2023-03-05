FROM python:3.9-slim as installer

RUN apt-get update
RUN apt-get install -y build-essential
RUN pip install -U pip wheel
RUN pip install poetry


WORKDIR /opt

RUN poetry config virtualenvs.in-project true --local
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root --only main

# Final stage
FROM python:3.9-slim

COPY --from=installer /opt/.venv /opt/.venv
ENV PATH=/opt/.venv/bin:$PATH

WORKDIR /opt/app

COPY webapp webapp
COPY app.py .
COPY preprocess_data.py .

EXPOSE 8000

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:server", "-b", "0.0.0.0", "--worker-tmp-dir", "/dev/shm", "--max-requests", "15", "--workers", "2" ]
