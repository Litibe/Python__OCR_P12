FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
VOLUME /app/log/
VOLUME /app/flake_rapport/
VOLUME /app/htmlcov/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
