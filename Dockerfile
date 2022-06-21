FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./docker_update_flake8html/plugin.py usr/lib/python3.10/site_packages/flake8-html/plugin.py
COPY . /app/
