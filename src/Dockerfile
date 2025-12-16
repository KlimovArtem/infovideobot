FROM python:3.13

WORKDIR usr/src/app

COPY ../.log-config.yaml ../.

COPY ../pyproject.toml ../.


COPY . .

WORKDIR usr/src 

RUN pip install -e . --no-cache-dir


CMD python src/bot/main.py

