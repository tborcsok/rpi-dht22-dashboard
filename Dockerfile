FROM python:3.12-slim as installer

COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

WORKDIR /opt

COPY pyproject.toml uv.lock /opt/

RUN uv sync --locked

# Final stage
FROM python:3.12-slim

COPY --from=installer /opt/.venv /opt/.venv
ENV PATH=/opt/.venv/bin:$PATH

WORKDIR /opt/app

COPY webapp webapp
COPY app.py .
COPY preprocess_data.py .

EXPOSE 8000

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:server", "-b", "0.0.0.0", "--worker-tmp-dir", "/dev/shm", "--max-requests", "15", "--threads", "2" ]
