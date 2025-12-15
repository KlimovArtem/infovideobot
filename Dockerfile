FROM python:3.13

WORKDIR usr/src/app

COPY .log-config.yaml .

COPY pyproject.toml .


COPY ./bot/. ./bot/

RUN pip install -e . --no-cache-dir

CMD python bot/main.py