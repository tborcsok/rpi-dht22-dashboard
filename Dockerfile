FROM python:3.9-slim

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install -U pip wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:server", "-b", "0.0.0.0", "--worker-tmp-dir", "/dev/shm" ]
